from django.http import HttpResponse, JsonResponse
from django.template import loader
import aai.suggestion as sgst

def index(request):
    template = loader.get_template('artoogle/index.html')
    return HttpResponse(template.render())


def search(request):
    search_terms = str(request.GET.get('arg')).lower()

    # Hilarious eastergg following
    if search_terms == 'bob ross':
        image_data = open("C:/Users/Naschinsui/PycharmProjects/aai/artoogle/static/artoogle/bob.jpg", "rb").read()
        return HttpResponse(image_data, content_type="image/png")

    # TODO: Query our backend

    return HttpResponse('You requested:   ' + search_terms)


def autosuggest(request):
    search_str = str(request.GET.get('arg')).lower() + '*'
    suggestions = sgst.search(search_str)
    return JsonResponse({'suggestions':suggestions})