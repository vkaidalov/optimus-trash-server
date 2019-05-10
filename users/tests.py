from django.test import TestCase
from .models import User
from .serializers import UserSerializer, ConfirmationSerializer


class UserSerializerTest(TestCase):
    def setUp(self):
        User.objects.create(
            username='vlad', password='hello_world', first_name='johnny')

    def test_with_full_data(self):
        data = {
            'username': 'sam',
            'password': 'twinkle_little_star',
            'email': 'sam@example.com',
            'first_name': 'Sam',
            'last_name': 'White'
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()

    def test_without_optional_data(self):
        data = {
            'username': 'john',
            'password': 'john_ce)nation',
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()

    def test_without_required_fields(self):
        data = {
        }
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_update_method(self):
        user = User.objects.get_by_natural_key('vlad')
        data = {
            'username': 'endpoint',
            'password': 'good',
            'first_name': 'nick',
            'last_name': 'bravo'
        }
        serializer = UserSerializer(user, data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()

    def test_update_method_with_bad_email(self):
        user = User.objects.get_by_natural_key('vlad')
        data = {
            'email': 'really bad email',
        }
        serializer = UserSerializer(user, data=data, partial=True)
        self.assertFalse(serializer.is_valid())


class ConfirmationSerializerTest(TestCase):
    def test_create(self):
        data = {
            'is_confirmed': True
        }
        serializer = ConfirmationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        is_confirmed = serializer.save()
        self.assertTrue(is_confirmed)

    def test_update(self):
        data = {
            'is_confirmed': False
        }
        is_confirmed = True
        serializer = ConfirmationSerializer(is_confirmed, data=data)
        self.assertTrue(serializer.is_valid())
        is_confirmed = serializer.save()
        self.assertFalse(is_confirmed)
