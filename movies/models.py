from itertools import count
from django.db import connection
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg

from authentication.models import User


class Genre(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    is_active = models.BooleanField(default=True)


class Movies(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    release_date = models.DateTimeField(blank=True, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.DO_NOTHING)
    plot = models.TextField(blank=False, null=False)
    image_banner = models.CharField(max_length=500, blank=True, null=True)
    image_poster = models.CharField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    # rating = GenericRelation(Rating, related_query_name='movies')


def raw_sqlquery():
    with connection.cursor() as cursor:
        cursor.execute(
            "select  (avg(raiting)) as rating, title, image_banner, image_poster, plot, genre_id, date(release_date) as release_date,movies_movies.id from movies_movies natural join movies_rating   group by  id, raiting, title,image_banner, image_poster, plot,release_date, genre_id, movies_movies.id")
        # row = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]


def raw_sqlquery_toprating():
    with connection.cursor() as cursor:
        cursor.execute("select  (avg(raiting)) as rating, title, image_banner, image_poster, plot, genre_id, "
                       "date(release_date) as release_date,movies_movies.id from movies_movies natural join "
                       "movies_rating  where raiting = 5 and movies_rating.is_active = true group by  id, raiting, "
                       "title,image_banner, image_poster, "
                       "plot,release_date, genre_id, movies_movies.id limit 7")
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]


class Rating(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.DO_NOTHING, related_name='rating')
    raiting = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=False, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


