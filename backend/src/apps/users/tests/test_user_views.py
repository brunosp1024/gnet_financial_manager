import pytest
from apps.users.tests.factories import UserFactory


LIST_URL = '/api/users/'


def DETAIL_URL(pk):
    return f'/api/users/{pk}/'
ME_URL     = '/api/users/me/'

@pytest.mark.django_db
class TestUserViewsAuthentication:
    def test_without_token_return_401(self, api_client):
        assert api_client.get(LIST_URL).status_code == 401

    def test_without_token_no_me_return_401(self, api_client):
        assert api_client.get(ME_URL).status_code == 401

@pytest.mark.django_db
class TestUserViewsAdmin:
    def test_list_users(self, admin_client):
        UserFactory.create_batch(3)
        res = admin_client.get(LIST_URL)
        assert res.status_code == 200
        assert res.data['count'] >= 3

    def test_create_user(self, admin_client):
        data = {
            'username':   'novo_user',
            'first_name': 'Novo',
            'last_name':  'User',
            'email':      'novo@test.com',
            'group':      'ADMIN',
            'password':   'senha@123',
        }
        res = admin_client.post(LIST_URL, data)
        assert res.status_code == 201
        assert res.data['email'] == 'novo@test.com'
        assert 'password' not in res.data

    def test_edit_user(self, admin_client, db):
        user = UserFactory()
        res = admin_client.patch(DETAIL_URL(user.pk), {'first_name': 'Editado'})
        assert res.status_code == 200
        assert res.data['first_name'] == 'Editado'

    def test_delete_user(self, admin_client, db):
        from apps.users.models import User
        user = UserFactory()
        pk = user.pk
        res = admin_client.delete(DETAIL_URL(pk))
        assert res.status_code == 204
        assert not User.objects.filter(pk=pk).exists()


@pytest.mark.django_db
class TestUserViewsFilters:
    def test_search_by_name(self, admin_client, db):
        UserFactory(first_name='Zacarias', last_name='Teste')
        UserFactory(first_name='Maria',    last_name='Teste')
        res = admin_client.get(LIST_URL, {'search': 'Zacarias'})
        assert res.status_code == 200
        assert res.data['count'] == 1
        assert res.data['results'][0]['first_name'] == 'Zacarias'

    def test_ordering_by_first_name(self, admin_client, db):
        UserFactory(first_name='Zebra')
        UserFactory(first_name='Abacate')
        res = admin_client.get(LIST_URL, {'ordering': 'first_name'})
        assert res.status_code == 200
        names = [r['first_name'] for r in res.data['results']]
        assert names == sorted(names)
