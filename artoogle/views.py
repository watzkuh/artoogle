import urllib

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
import aai.suggestion as sgst
import aai.query as query

pool = query.RDFQueries()


def index(request):
    template = loader.get_template('artoogle/index.html')
    return HttpResponse(template.render())


def search(request):
    search_terms = str(request.GET.get('arg'))

    # Hilarious eastergg following
    if search_terms == 'bob ross':
        image_data = open("C:/Users/Naschinsui/PycharmProjects/aai/artoogle/static/artoogle/bob.jpg", "rb").read()
        return HttpResponse(image_data, content_type="image/png")

    abstract = pool.get_abstract(search_terms)
    images = pool.get_art(search_terms)

    return render(request, 'artoogle/index.html', {
        'abstract': abstract,
        'images': images
    })


def autosuggest(request):
    search_str = str(request.GET.get('arg')) + '*'
    suggestions = sgst.search(search_str)
    return JsonResponse({'suggestions': suggestions})
