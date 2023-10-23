from rest_framework import routers
from movies_collection.v1.api import CollectionView, ListMoviesView
from django.urls import path, include
router = routers.DefaultRouter()
router.register('collection', CollectionView, 'collection')
router.register('movies', ListMoviesView, 'movies')

urlpatterns = [
    path('', include(router.urls)),

]