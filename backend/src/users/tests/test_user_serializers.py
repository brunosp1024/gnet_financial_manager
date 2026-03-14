import pytest
from django.contrib.auth.models import Group
from rest_framework.test import APIRequestFactory

from users.serializers import (
    UserCreateSerializer,
    UserDetailSerializer,
    UserListSerializer,
    UserUpdateSerializer,
)
from users.tests.factories import UserFactory


def make_request(user, method='post'):
    factory = APIRequestFactory()
    request = getattr(factory, method)('/')
    request.user = user
    return request


# ── UserCreateSerializer ───────────────────────────────────────────────────────

@pytest.mark.django_db
class TestUserCreateSerializer:

    def _valid_data(self, group_name='ADMIN'):
        return {
            'username':   'novo_user',
            'first_name': 'Novo',
            'last_name':  'User',
            'email':      'novo@example.com',
            'group':      group_name,
            'password':   'senha@123',
            'is_active':  True,
        }

    def test_valid_create_saves_user(self, admin_user):
        s = UserCreateSerializer(
            data=self._valid_data(),
            context={'request': make_request(admin_user)},
        )
        assert s.is_valid(), s.errors
        user = s.save()
        assert user.pk is not None
        assert user.username == 'novo_user'
        assert user.groups.filter(name='ADMIN').exists()

    def test_password_is_hashed(self, admin_user):
        s = UserCreateSerializer(
            data=self._valid_data(),
            context={'request': make_request(admin_user)},
        )
        assert s.is_valid(), s.errors
        user = s.save()
        assert user.check_password('senha@123')
        assert not user.password.startswith('senha@123')

    def test_created_by_and_updated_by_set_from_request(self, admin_user):
        s = UserCreateSerializer(
            data=self._valid_data(),
            context={'request': make_request(admin_user)},
        )
        assert s.is_valid(), s.errors
        user = s.save()
        assert user.created_by == admin_user
        assert user.updated_by == admin_user

    def test_password_is_write_only(self, admin_user):
        s = UserCreateSerializer(
            data=self._valid_data(),
            context={'request': make_request(admin_user)},
        )
        assert s.is_valid(), s.errors
        s.save()
        assert 'password' not in s.data

    def test_group_is_write_only(self, admin_user):
        s = UserCreateSerializer(
            data=self._valid_data(),
            context={'request': make_request(admin_user)},
        )
        assert s.is_valid(), s.errors
        s.save()
        assert 'group' not in s.data

    def test_readonly_fields_ignored_on_input(self, admin_user, financeiro_user):
        data = self._valid_data()
        data['created_by'] = str(financeiro_user.pk)
        data['created_at'] = '2000-01-01T00:00:00Z'
        s = UserCreateSerializer(
            data=data,
            context={'request': make_request(admin_user)},
        )
        assert s.is_valid(), s.errors
        user = s.save()
        assert user.created_by == admin_user

    def test_duplicate_email_is_invalid(self, admin_user):
        UserFactory(email='dup@example.com')
        data = self._valid_data()
        data['email'] = 'dup@example.com'
        s = UserCreateSerializer(
            data=data,
            context={'request': make_request(admin_user)},
        )
        assert not s.is_valid()
        assert 'email' in s.errors

    def test_weak_password_is_invalid(self, admin_user):
        data = self._valid_data()
        data['password'] = 'abc'
        s = UserCreateSerializer(
            data=data,
            context={'request': make_request(admin_user)},
        )
        assert not s.is_valid()
        assert 'password' in s.errors

    def test_numeric_only_password_is_invalid(self, admin_user):
        data = self._valid_data()
        data['password'] = '12345678'
        s = UserCreateSerializer(
            data=data,
            context={'request': make_request(admin_user)},
        )
        assert not s.is_valid()
        assert 'password' in s.errors

    def test_missing_required_fields(self, admin_user):
        s = UserCreateSerializer(
            data={},
            context={'request': make_request(admin_user)},
        )
        assert not s.is_valid()
        for field in ('username', 'password', 'group'):
            assert field in s.errors

    def test_invalid_group_is_rejected(self, admin_user):
        data = self._valid_data()
        data['group'] = 'INEXISTENTE'
        s = UserCreateSerializer(
            data=data,
            context={'request': make_request(admin_user)},
        )
        assert not s.is_valid()
        assert 'group' in s.errors


# ── UserDetailSerializer ───────────────────────────────────────────────────────

@pytest.mark.django_db
class TestUserDetailSerializer:

    def test_returns_expected_fields(self, admin_user):
        user = UserFactory(groups=['ADMIN'], created_by=admin_user, updated_by=admin_user)
        s = UserDetailSerializer(user)
        expected = {
            'username', 'first_name', 'last_name', 'email', 'group',
            'is_active', 'created_at', 'updated_at', 'created_by', 'updated_by',
        }
        assert expected == set(s.data.keys())

    def test_group_returns_name(self, admin_user):
        s = UserDetailSerializer(admin_user)
        assert s.data['group'] == 'ADMIN'

    def test_group_returns_none_when_no_group(self, no_group_user):
        s = UserDetailSerializer(no_group_user)
        assert s.data['group'] is None

    def test_created_by_returns_full_name(self, admin_user):
        user = UserFactory(groups=['GERENTE'], created_by=admin_user)
        s = UserDetailSerializer(user)
        assert s.data['created_by'] == admin_user.get_full_name()

    def test_updated_by_returns_full_name(self, admin_user, gerente_user):
        user = UserFactory(groups=['FINANCEIRO'], updated_by=gerente_user)
        s = UserDetailSerializer(user)
        assert s.data['updated_by'] == gerente_user.get_full_name()


# ── UserUpdateSerializer ───────────────────────────────────────────────────────

@pytest.mark.django_db
class TestUserUpdateSerializer:

    def test_valid_update_changes_fields(self, admin_user, gerente_user):
        s = UserUpdateSerializer(
            gerente_user,
            data={'first_name': 'Novo', 'last_name': 'Nome'},
            partial=True,
            context={'request': make_request(admin_user)},
        )
        assert s.is_valid(), s.errors
        user = s.save()
        assert user.first_name == 'Novo'
        assert user.last_name == 'Nome'

    def test_updated_by_is_set_from_request(self, admin_user, gerente_user):
        s = UserUpdateSerializer(
            gerente_user,
            data={'first_name': 'X'},
            partial=True,
            context={'request': make_request(admin_user)},
        )
        assert s.is_valid(), s.errors
        user = s.save()
        assert user.updated_by == admin_user

    def test_password_updated_and_hashed_when_provided(self, admin_user, gerente_user):
        s = UserUpdateSerializer(
            gerente_user,
            data={'password': 'novaSenha@456'},
            partial=True,
            context={'request': make_request(admin_user)},
        )
        assert s.is_valid(), s.errors
        user = s.save()
        assert user.check_password('novaSenha@456')

    def test_password_not_changed_when_not_provided(self, admin_user, gerente_user):
        old_password_hash = gerente_user.password
        s = UserUpdateSerializer(
            gerente_user,
            data={'first_name': 'Qualquer'},
            partial=True,
            context={'request': make_request(admin_user)},
        )
        assert s.is_valid(), s.errors
        user = s.save()
        assert user.password == old_password_hash

    def test_group_updated_when_provided(self, admin_user, gerente_user):
        s = UserUpdateSerializer(
            gerente_user,
            data={'group': 'FINANCEIRO'},
            partial=True,
            context={'request': make_request(admin_user)},
        )
        assert s.is_valid(), s.errors
        user = s.save()
        assert user.groups.filter(name='FINANCEIRO').exists()
        assert not user.groups.filter(name='GERENTE').exists()

    def test_group_not_changed_when_not_provided(self, admin_user, gerente_user):
        s = UserUpdateSerializer(
            gerente_user,
            data={'first_name': 'X'},
            partial=True,
            context={'request': make_request(admin_user)},
        )
        assert s.is_valid(), s.errors
        s.save()
        assert gerente_user.groups.filter(name='GERENTE').exists()

    def test_duplicate_email_is_invalid(self, admin_user, gerente_user):
        other = UserFactory(email='taken@example.com')
        s = UserUpdateSerializer(
            gerente_user,
            data={'email': other.email},
            partial=True,
            context={'request': make_request(admin_user)},
        )
        assert not s.is_valid()
        assert 'email' in s.errors

    def test_same_email_on_same_user_is_valid(self, admin_user, gerente_user):
        s = UserUpdateSerializer(
            gerente_user,
            data={'email': gerente_user.email},
            partial=True,
            context={'request': make_request(admin_user)},
        )
        assert s.is_valid(), s.errors

    def test_duplicate_username_is_invalid(self, admin_user, gerente_user):
        other = UserFactory()
        s = UserUpdateSerializer(
            gerente_user,
            data={'username': other.username},
            partial=True,
            context={'request': make_request(admin_user)},
        )
        assert not s.is_valid()
        assert 'username' in s.errors

    def test_same_username_on_same_user_is_valid(self, admin_user, gerente_user):
        s = UserUpdateSerializer(
            gerente_user,
            data={'username': gerente_user.username},
            partial=True,
            context={'request': make_request(admin_user)},
        )
        assert s.is_valid(), s.errors

    def test_weak_password_is_invalid(self, admin_user, gerente_user):
        s = UserUpdateSerializer(
            gerente_user,
            data={'password': 'abc'},
            partial=True,
            context={'request': make_request(admin_user)},
        )
        assert not s.is_valid()
        assert 'password' in s.errors

    def test_password_is_write_only(self, admin_user, gerente_user):
        s = UserUpdateSerializer(
            gerente_user,
            data={'password': 'novaSenha@456'},
            partial=True,
            context={'request': make_request(admin_user)},
        )
        assert s.is_valid(), s.errors
        s.save()
        assert 'password' not in s.data

    def test_group_is_write_only(self, admin_user, gerente_user):
        s = UserUpdateSerializer(
            gerente_user,
            data={'group': 'FINANCEIRO'},
            partial=True,
            context={'request': make_request(admin_user)},
        )
        assert s.is_valid(), s.errors
        s.save()
        assert 'group' not in s.data


# ── UserListSerializer ─────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestUserListSerializer:

    def test_returns_expected_fields(self, admin_user):
        s = UserListSerializer(admin_user)
        expected = {'id', 'first_name', 'last_name', 'email', 'group', 'is_active', 'created_at'}
        assert expected == set(s.data.keys())

    def test_id_is_present(self, admin_user):
        s = UserListSerializer(admin_user)
        assert str(s.data['id']) == str(admin_user.pk)

    def test_group_returns_name(self, admin_user):
        s = UserListSerializer(admin_user)
        assert s.data['group'] == 'ADMIN'

    def test_group_returns_none_when_no_group(self, no_group_user):
        s = UserListSerializer(no_group_user)
        assert s.data['group'] is None

    def test_many_serialization(self, admin_user, gerente_user):
        users = [admin_user, gerente_user]
        s = UserListSerializer(users, many=True)
        assert len(s.data) == 2
