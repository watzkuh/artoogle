import urllib

import deepl
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader

import aai.autosuggest as sgst
import aai.query as query
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
    search_terms = search_terms.replace('%28', '(')
    search_terms = search_terms.replace('%29', ')')

    # Hilarious eastergg following
    if search_terms == 'bob_ross':
        webite = '<head><meta http-equiv="refresh" content="0; url=https://geekandsundry.com/wp-content/uploads/' \
                 '2017/07/Bob-Ross-The-Art-of-Chill-featured.jpg"/></head>'
        return HttpResponse(webite, content_type="text")

    abstract = pool.get_abstract(search_terms)
    images = pool.get_art_from_artist(search_terms)
    log = logLoader.get_log(get_client_ip(request))
    if search_terms:
        log.add_search(search_terms)

    lang = request.COOKIES.get('lang')
    if lang in languages:
        abstract, _ = deepl.translate(abstract, source='EN', target=lang)
        # for path, title in images.items():
        # images[path], _ = deepl.translate(title, source='EN', target=lang)

    recommendations = recommender.get_recommendations(get_client_ip(request))
    print("recommendations für ", get_client_ip(request))
    print(recommendations)
    print(images)
    return render(request, 'artoogle/index.html', {
        'abstract': abstract,
        'images': images,
        'recommendations': recommendations
    })


def detail(request):
    # artwork contatins the artwork's name that was klicked on, i.e. "Starry Night Over the Rhone"
    artwork = str(request.GET.get('arg'))

    images = pool.get_similar_art(artwork, 5)
    labels = pool.get_artwork_labels(artwork)

    return render(request, 'artoogle/detail.html', {
        'images': images,
        'labels': labels,
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
