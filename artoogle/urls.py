from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('autosuggest', views.auto_suggest, name='autosuggest'),
    path('runindex', views.run_index, name='runindex'),
]
