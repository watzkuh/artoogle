from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template('artoogle/index.html')
    return HttpResponse(template.render())


def search(request):
    search_terms = str(request.GET.get('arg'))

    # TODO: Query our backend

    return HttpResponse('You requested:   ' + search_terms)
