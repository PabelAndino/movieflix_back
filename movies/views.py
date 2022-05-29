from django.shortcuts import render
from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, action
from django.db import connection
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404, ListCreateAPIView, ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from authentication.views import IsSuperUser
from .models import Genre, Movies, Rating, raw_sqlquery, raw_sqlquery_toprating
from .serializers import GenreSerializer, GenreDisableSerializer, MoviesSerializer, MovieDisableSerializer, \
    RatingSerializer, RatingDisableComment, MoviesRatingSerializer, MoviesByDateSerializer, DisableRatingSerializer


class GenreViewSet(viewsets.ViewSet):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated, IsSuperUser]

    @swagger_auto_schema(request_body=GenreSerializer)
    def create(self, request):
        try:
            serializer = GenreSerializer(data=request.data, context={"request", request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = {'error': False, 'detail': 'Genre Saved Successfully'}

        except:
            response = {'error': True, 'detail': serializer.errors}

        return Response(response)

    def list(self, request):
        genre = Genre.objects.filter(is_active=True)
        serializer = GenreSerializer(genre, many=True, context={'request': request})
        response = {
            'error': False,
            'message': 'All genres',
            'data': serializer.data
        }

        return Response(response)

    @swagger_auto_schema(request_body=GenreDisableSerializer)
    @action(detail=False, methods=['patch'], url_path=r'disable/(?P<pk>\w+)', name='Disable Genre')
    def disable_genre(self, request, pk=None):
        try:
            query_set = Genre.objects.all()
            genre = get_object_or_404(query_set, pk=pk)
            serializer = GenreDisableSerializer(genre, data=request.data, context={'request': request}, required=False)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = {'error': False, 'detail': 'Genre disable correctly'}
        except:
            response = {
                'error': True,
                'detail': serializer.errors
            }

        return Response(response)

    @swagger_auto_schema(request_body=GenreSerializer)
    def update(self, request, pk=None):
        try:
            queryset = Genre.objects.all()
            genre = get_object_or_404(queryset, pk=pk)
            serializer = GenreSerializer(genre, data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = {'error': False, 'detail': 'Genre updated successfully'}
        except:
            response = {'error': True, 'detail': serializer.errors}

        return Response(response)

class MovieViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperUser]

    @swagger_auto_schema(request_body=MoviesSerializer)
    def create(self, request):
        try:
            serializer = MoviesSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = {'error': False, 'detail': 'Movie saved successfully'}

        except:
            response = {'error': True, 'detail': serializer.errors}

        return Response(response)

    def list(self, request):
        movies = Movies.objects.filter(is_active=True)
        serializer = MoviesSerializer(movies, many=True, context={'request', request})
        response = {
            'error': False,
            'detail': serializer.data
        }
        return Response(response)

    @swagger_auto_schema(request_body=MovieDisableSerializer)
    @action(detail=False, methods=['patch'], url_path=r'disable/(?P<pk>\w+)', name='Disable Movie')
    def disable_movie(self, request, pk=None):
        try:
            queryset = Movies.objects.all()
            movies = get_object_or_404(queryset, pk=pk)
            serializer = MovieDisableSerializer(movies, data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = {'error': False, 'detail': 'Movie disabled correctly'}
        except:
            response = {'error': True, 'detail': serializer.errors}

        return Response(response)

    @swagger_auto_schema(request_body=MoviesSerializer)
    def update(self, request, pk=None):
        try:
            queryset = Movies.objects.all()
            movies = get_object_or_404(queryset, pk=pk)
            serializer = MoviesSerializer(movies, data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = {'error': False, 'detail': 'Movie updated successfully'}
        except:
            response = {'error': True, 'detail': serializer.errors}
        return Response(response)


class RatingListAPIView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = RatingSerializer
    queryset = Rating.objects.all()

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class MovieSearchName(ListAPIView):
    serializer_class = MoviesSerializer

    def get_queryset(self):
        title = self.kwargs["title"]
        return Movies.objects.filter(title__contains=title)


class CommentsViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        comments = Rating.objects.filter(is_active=True)

        serializer = RatingSerializer(comments, many=True, context={'request', request})
        response = {
            'error': False,
            'detail': serializer.data
        }
        return Response(response)

    @swagger_auto_schema(request_body=DisableRatingSerializer)
    @action(detail=False, methods=['patch'], url_path=r'disable/(?P<pk>\w+)', name='Disable Rating')
    def disable_rating(self, request, pk=None):
        try:
            query_set = Rating.objects.all()
            rating = get_object_or_404(query_set, pk=pk)
            serializer = DisableRatingSerializer(rating, data=request.data, context={'request': request}, required=False)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = {'error': False, 'detail': 'Rating disable correctly'}
        except:
            response = {
                'error': True,
                'detail': serializer.errors
            }

        return Response(response)

class RatingViewSet(viewsets.ViewSet):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=RatingSerializer)
    def create(self, request):

        try:
            serializer_class = RatingSerializer(data=request.data, context={'request': request})
            serializer_class.is_valid(raise_exception=True)
            serializer_class.save()
            response = {'error': False, 'detail': 'Rating successfully'}

        except:
            response = {'error': True, 'detail': serializer_class.errors}

        return Response(response)

    def list(self, request):
        rating = Rating.objects.filter(is_active=True)
        serializer = RatingSerializer(rating, many=True, context={'request', request})
        response = {
            'error': False,
            'detail': serializer.data
        }
        return Response(response)

    @swagger_auto_schema(request_body=RatingDisableComment)
    @action(detail=False, methods=['patch'], url_path=r'disable/(?P<pk>\w+)', name='Disable Comment')
    def disable_rating(self, request, pk=None):
        try:
            queryset = Rating.objects.all()
            rating = get_object_or_404(queryset, pk=pk)
            serializer = RatingDisableComment(rating, data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = {'error': False, 'detail': 'Rating deleted correctly'}
        except:
            response = {'error': True, 'detail': serializer.errors}

        return Response(response)

    @swagger_auto_schema(request_body=RatingSerializer)
    def update(self, request, pk=None):
        try:
            queryset = Rating.objects.all()
            rating = get_object_or_404(queryset, pk=pk)
            serializer = RatingSerializer(rating, data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = {'error': False, 'detail': 'Rating updated successfully'}
        except:
            response = {'error': True, 'detail': serializer.errors}
        return Response(response)

class RatingByMovieViewSet(ListAPIView):
    serializer_class = RatingSerializer

    def get_queryset(self):
        movie = self.kwargs["movie"]
        return Rating.objects.filter(movie_id=movie)

class MovieGeneralViewset(viewsets.ViewSet):

    def list(self, request):
        movies = raw_sqlquery()

        genres = Genre.objects.filter(is_active=True)
        serializer_genre = GenreSerializer(genres, many=True, context={'request': request})
        # serializer = MoviesRatingSerializer(movies, many=True, context={'request', request})
        response = {
            'error': False,
            'detail': {'data': {
                'movies': [movies],  # serializer.data

            },
                'genres': serializer_genre.data
            }
        }
        return Response(response)

class MovieGeneralSimpleViewset(viewsets.ViewSet):

    def list(self, request):
        movies = raw_sqlquery()

        genres = Genre.objects.filter(is_active=True)
        serializer_genre = GenreSerializer(genres, many=True, context={'request': request})
        # serializer = MoviesRatingSerializer(movies, many=True, context={'request', request})
        response = {
            'error': False,
            'detail': movies
        }
        return Response(response)


class MovieTopRatingViewset(viewsets.ViewSet):

    def list(self, request):
        movies = raw_sqlquery_toprating()
        genres = Genre.objects.filter(is_active=True)
        serializer_genre = GenreSerializer(genres, many=True, context={'request': request})
        # serializer = MoviesRatingSerializer(movies, many=True, context={'request', request})
        response = {
            'error': False,
            'detail': movies
        }
        return Response(response)

class MoviesByDate(viewsets.ViewSet):
    def list(self, request):
        movies = Movies.objects.filter(is_active=True).order_by('-release_date')[:7]
        serializer = MoviesByDateSerializer(movies, many=True, context={'request', request})
        response = {
            'error': False,
            'detail': serializer.data
        }
        return Response(response)

class SearchMovies(viewsets.ViewSet):
    def list(self, request):
        movies = Movies.objects.filter(is_active=True)
        serializer = MoviesSerializer(movies, many=True, context={'request', request})
        filter_backends = (SearchFilter,)
        search_fields = ['username', 'email']
        response = {
            'error': False,
            'detail': serializer.data
        }
        return Response(response)


