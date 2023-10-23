from rest_framework import viewsets, mixins, status, serializers
from rest_framework.decorators import action
from requests.auth import HTTPBasicAuth
from movies_collection.models import MovieCollection, Movie
from rest_framework.permissions import IsAuthenticated
from movies_collection.v1.serializers import MovieCollectionSerializer, CreateCollectionSerializer
from rest_framework.response import Response
from movies_collection.utils import http_adapter
from decouple import config
from django.db.models import Count

class CollectionView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    
    lookup_field = 'collection_uuid'
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'retrieve']:
            return CreateCollectionSerializer
        return MovieCollectionSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
    def get_queryset(self):
        return MovieCollection.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        collection = serializer.create(request.data)
        serializer = MovieCollectionSerializer(collection)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        genres = Movie.objects.filter(user=request.user).annotate(
            qty=Count('genres')).order_by('-qty').distinct()[:3]
        
        top_genres = ', '.join(key.genres  for key in genres) if genres else ''

        data ={'is_success':True, 'data':{'collection':serializer.data, 'favourite_genres': top_genres}
               }
        return Response(data, status=status.HTTP_200_OK)



class ListMoviesView(viewsets.GenericViewSet):
    serializer_class = serializers.Serializer
    queryset=Movie.objects.none()
    authentication_classes=[IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        movie_url = config('BASE_CREADY_URL') +'/api/v1/maya/movies/'
        response = http_adapter.get(movie_url, auth=HTTPBasicAuth(config('CREADY_USER_NAME'), config('CREADY_PASSWORD')), verify=False)
        return Response(response.json(), status=status.HTTP_200_OK)