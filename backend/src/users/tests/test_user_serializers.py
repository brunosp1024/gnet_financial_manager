import pytest
from rest_framework.test import APIRequestFactory
from users.serializers import UserSerializer


def make_request(user):
    factory = APIRequestFactory()
    request = factory.get('/')
    request.user = user
    return request

@pytest.mark.django_db
class TestUserSerializer:
    def test_fields_read_only_not_accept_write(self, admin_user):
        request = make_request(admin_user)
        data = {
            'username':   'user_test',
            'first_name': 'Test',
            'last_name':  'User',
            'email':      'test@test.com',
            'password':   'senha@123',
            'created_at': '2020-01-01T00:00:00Z',
            'created_by': str(admin_user.pk),
        }
        serializer = UserSerializer(data=data, context={'request': request})
        assert serializer.is_valid(), serializer.errors
        user = serializer.save()
        assert user.created_by == admin_user

    def test_password_not_in_response(self, admin_user):
        serializer = UserSerializer(admin_user)
        assert 'password' not in serializer.data

    def test_password_is_hashed_on_create(self, admin_user):
        request = make_request(admin_user)
        data = {
            'username':   'hash_test',
            'first_name': 'Hash',
            'last_name':  'Test',
            'email':      'hash@test.com',
            'password':   'senha@123',
        }
        serializer = UserSerializer(data=data, context={'request': request})
        assert serializer.is_valid(), serializer.errors
        user = serializer.save()
        assert user.check_password('senha@123')
        assert not user.password.startswith('senha@123')
