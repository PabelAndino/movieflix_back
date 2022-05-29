from django.urls import path
from .views import RatingListAPIView, MovieSearchName, RatingByMovieViewSet

urlpatterns = [
    path('api/rating/', RatingListAPIView.as_view(), name='rating'),
    path('api/movie_name/<str:title>/', MovieSearchName.as_view(), name='movie_name'),
    path('api/rating_bymovie/<int:movie>/', RatingByMovieViewSet.as_view(), name='movie_ratingbyname')
]
