from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Avg, Count, Q
from rest_framework import serializers
from .models import Genre, Movies, Rating
from authentication.models import User


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class MoviesSerializer(serializers.ModelSerializer):
    release_date = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")

    class Meta:
        model = Movies
        fields = '__all__'


class MoviesByDateSerializer(serializers.ModelSerializer):
    genre = serializers.CharField(source='genre.name')
    release_date = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")

    class Meta:
        model = Movies
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    user_firstname = serializers.ReadOnlyField(source='owner.first_name')


    class Meta:
        model = Rating
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['movie'] = MoviesSerializer(instance.movie).data
        return response


class DisableRatingSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(required=True)

    class Meta:
        model = Rating
        fields = ['is_active']


class MoviesRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = ['id', 'title', 'all_rating']


class MovieDisableSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(required=True)

    class Meta:
        model = Movies
        fields = ['is_active']


class GenreDisableSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(required=True)

    class Meta:
        model = Genre
        fields = ['is_active']


class RatingDisableComment(serializers.ModelSerializer):
    is_active = serializers.BooleanField(required=True)

    class Meta:
        model = Genre
        fields = ['is_active']
