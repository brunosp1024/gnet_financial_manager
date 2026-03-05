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

    def test_created_by_filled_by_mixin(self, admin_user):
        request = make_request(admin_user)
        data = {
            'username':   'novo_user',
            'first_name': 'Novo',
            'last_name':  'User',
            'email':      'novo@test.com',
            'password':   'senha@123',
        }
        serializer = UserSerializer(data=data, context={'request': request})
        assert serializer.is_valid(), serializer.errors
        user = serializer.save()
        assert user.created_by == admin_user
        assert user.updated_by == admin_user

    def test_updated_by_filled_on_update(self, admin_user, financeiro_user):
        request = make_request(financeiro_user)
        serializer = UserSerializer(
            admin_user,
            data={'first_name': 'Editado'},
            partial=True,
            context={'request': request},
        )
        assert serializer.is_valid(), serializer.errors
        serializer.save()
        admin_user.refresh_from_db()
        assert admin_user.updated_by == financeiro_user

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
