import urllib

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
import aai.suggestion as sgst
import aai.query as query
import deepl

from aai.log.ArtistRecommendation import ArtistRecommendation
from aai.log.LogLoader import LogLoader

pool = query.RDFQueries()
languages = ['DE', 'FR', 'ES', 'IT', 'NL', 'PL']

recommender = ArtistRecommendation(pool)
logLoader = LogLoader()
logLoader.register(0, recommender)

def index(request):
    template = loader.get_template('artoogle/index.html')
    return HttpResponse(template.render())


def search(request):
    search_terms = str(request.GET.get('arg'))
    search_terms = search_terms.replace(' ', '_')
    search_terms = urllib.parse.quote(search_terms)
    # Hilarious eastergg following
    if search_terms == 'bob ross':
        image_data = open("C:/Users/Naschinsui/PycharmProjects/aai/artoogle/static/artoogle/bob.jpg", "rb").read()
        return HttpResponse(image_data, content_type="image/png")

    abstract = pool.get_abstract(search_terms)
    images = pool.get_art(search_terms)
    log = logLoader.get_log(get_client_ip(request))
    log.add_search(search_terms)

    lang = request.COOKIES.get('lang')
    if lang in languages:
        abstract, _ = deepl.translate(abstract, source='EN', target=lang)
        #for path, title in images.items():
            # images[path], _ = deepl.translate(title, source='EN', target=lang)

    recommendations = recommender.get_recommendations(get_client_ip(request))
    print("recommendations für ", get_client_ip(request))
    print(recommendations)

    return render(request, 'artoogle/index.html', {
        'abstract': abstract,
        'images': images,
        'recommendations' : recommendations
    })


def auto_suggest(request):
    search_str = str(request.GET.get('arg'))
    suggestions = sgst.search(search_str)
    return JsonResponse({'suggestions': suggestions})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def run_index(request):
    sgst.full_index()
    return HttpResponse("done")
