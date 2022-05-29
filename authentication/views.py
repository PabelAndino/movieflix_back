from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import  action
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from authentication.serializers import UserSerializer, ManageUserSerializer, DisableUserSerializer
from .models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['is_superuser'] = user.is_superuser
        token['user_image'] = user.user_image
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class IsSuperUser(BasePermission):
    """
    Allows access only to superusers.
    """

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return False


class UserView(viewsets.ViewSet):
    # @swagger_auto_schema(request_body=UserSerializer)
    def list(self, request):
        users = User.objects.filter(is_active=True)
        serializer = UserSerializer(users, many=True, context={'request': request})
        response = {
            'error': False,
            'message': 'Todos los Usuarios',
            'data': serializer.data
        }

        return Response(response)


class ManageUserView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperUser]

    def list(self, request):
        users = User.objects.filter(is_active=True)
        serializer = ManageUserSerializer(users, many=True, context={'request': request})
        response = {
            'error': False,
            'message': 'All User',
            'data': serializer.data
        }

        return Response(response)

    @swagger_auto_schema(request_body=ManageUserSerializer)
    def create(self, request):

        try:
            serializer = ManageUserSerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = {'error': False, 'detail': 'User Created Correctly'}
        except :
            response = {'error': True, 'detail': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST}

        return Response(response)

    @swagger_auto_schema(request_body=DisableUserSerializer)
    @action(detail=False, methods=['patch'], url_path=r'disable/(?P<pk>\w+)', name='Disable User')
    def disable_user(self, request, pk=None):
        try:
            queryset = User.objects.all()
            user = get_object_or_404(queryset, pk=pk)
            serializer = DisableUserSerializer(user, data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = {'Error': False, 'message': 'User desactivated'}

        except:
            response = {'Error': True, 'message': serializer.errors}

        return Response(response)

    @swagger_auto_schema(request_body=ManageUserSerializer)
    def update(self, request, pk=None):
        query_set = User.objects.all()
        user = get_object_or_404(query_set, pk=pk)
        serializer = ManageUserSerializer(user, data=request.data, context={'request': request})
        try:
            serializer.is_valid()
            serializer.save()
            dict_response = {
                'error': False,
                'message': 'User Updated correctly'
            }
        except:
            dict_response = {
                'error': True,
                'message': serializer.errors
            }

        return Response(dict_response)