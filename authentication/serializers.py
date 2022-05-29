from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'user_image']
        # read_only_fields = ['first_name', 'last_name', 'user_image']


class ManageUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_superuser', 'password','user_image']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)




class ManageUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_superuser', 'password', 'user_image']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class DisableUserSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(required=True)

    class Meta:
        model = User
        fields = ['is_active']
