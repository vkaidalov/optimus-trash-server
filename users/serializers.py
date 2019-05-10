from rest_framework import serializers
from .models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'password', 'email', 'date_joined',
                  'first_name', 'last_name', 'is_confirmed',)
        read_only_fields = ('is_confirmed', 'date_joined')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )

        user.set_password(validated_data['password'])

        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        instance.save()
        return instance


class ConfirmationSerializer(serializers.Serializer):
    is_confirmed = serializers.BooleanField(required=True)

    def create(self, validated_data):
        return validated_data['is_confirmed']

    def update(self, instance, validated_data):
        instance = validated_data['is_confirmed']
        return instance
