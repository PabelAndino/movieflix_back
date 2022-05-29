"""movieflix_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions, routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (TokenRefreshView, )
from authentication.views import MyTokenObtainPairView, UserView, ManageUserView
from movies.views import GenreViewSet, MovieViewSet, MovieGeneralViewset, RatingListAPIView, RatingViewSet, \
    MoviesByDate, MovieTopRatingViewset, CommentsViewSet, MovieGeneralSimpleViewset

schema_view = get_schema_view(
    openapi.Info(
        title="MovieFlix  API",
        default_version='v1',
        description="Data for consume ",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="pabelandino@gmail.com"),
        license=openapi.License(name="License of use"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register("user", UserView, basename='user')
router.register("manage_user", ManageUserView, basename='manage_user')

router.register('genre', GenreViewSet, basename='genre')
router.register('movies', MovieViewSet, basename='movies')
router.register('movies_general', MovieGeneralViewset, basename='movies_general')
router.register('movies_simple', MovieGeneralSimpleViewset, basename='movies_simple')
router.register('movies_bydate', MoviesByDate, basename='movies_bydate')
router.register('movies_toprating', MovieTopRatingViewset, basename='movies_toprating')
router.register('comments', CommentsViewSet, basename='comments')
#router.register('rating', RatingViewSet, basename='rating')
# router.register('rating', RatingListAPIView.as_view(), basename='rating')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', include('movies.urls')),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
