from . views import index, searchword, Results
from django.urls import path, include

urlpatterns = [
    path('', index, name= 'index'), #path to search view.
    path('search/', searchword, name = 'searchword'), #path to autocomplete
    path('jsonoutput/', Results, name='Results'), #path to search results
]