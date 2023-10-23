from rest_framework import serializers

from movies_collection.models import Movie, MovieCollection

class MovieCollectionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MovieCollection
        fields='__all__'



class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title', 'description', 'genres', 'uuid')


class CreateCollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True)
    class Meta:
        model = MovieCollection
        fields = ('title', 'description', 'movies')
    
    def create(self, validated_data):
        user = self.context.get('request').user
        collection = MovieCollection.objects.create(
            title=validated_data.get('title'), description=validated_data.get('description'),
            user=user
        )
        for movie in validated_data.get('movies'):
            movies= Movie.objects.filter(uuid=movie.get('uuid'), user=user, collection=collection).first() or Movie()
            movies.title = movie.get('title')
            movies.description = movie.get('description')
            movies.genres = movie.get('genres')
            movies.uuid= movie.get('uuid')
            movies.collection = collection
            movies.user = user
            movies.save()
        return collection
        
    def update(self, instance, validated_data):
        user = self.context.get('request').user
        instance.title=validated_data.get('title')
        instance.description=validated_data.get('description')
        instance.save()
        for movie in validated_data.get('movies'):
            movies= Movie.objects.filter(uuid=movie.get('uuid'), user=user, collection=instance).first() or Movie()
            movies.title = movie.get('title')
            movies.description = movie.get('description')
            movies.genres = movie.get('genres')
            movies.uuid= movie.get('uuid')
            movies.collection = instance
            movies.user = user
            movies.save()
        return instance
        
