import pytest
from customers.tests.factories import CustomerFactory

LIST_URL = '/api/customers/'


def DETAIL_URL(pk):
    return f'/api/customers/{pk}/'


@pytest.mark.django_db
class TestCustomerViewsAutenticacao:

    def test_sem_token_retorna_401(self, api_client):
        assert api_client.get(LIST_URL).status_code == 401

    def test_sem_grupo_retorna_403(self, no_group_client):
        assert no_group_client.get(LIST_URL).status_code == 403


@pytest.mark.django_db
class TestCustomerViewsPermissoes:

    def test_admin_lista(self, admin_client):
        CustomerFactory.create_batch(2)
        res = admin_client.get(LIST_URL)
        assert res.status_code == 200

    def test_financeiro_lista(self, financeiro_client):
        res = financeiro_client.get(LIST_URL)
        assert res.status_code == 200

    def test_financeiro_cria(self, financeiro_client):
        data = {'name': 'Cliente Financeiro', 'start_date': '2024-01-01'}
        res = financeiro_client.post(LIST_URL, data)
        assert res.status_code == 201

    def test_financeiro_edita(self, financeiro_client, db):
        c = CustomerFactory()
        res = financeiro_client.patch(DETAIL_URL(c.pk), {'name': 'Editado'})
        assert res.status_code == 200

    def test_financeiro_deleta(self, financeiro_client, db):
        from customers.models import Customer
        c = CustomerFactory()
        pk = c.pk
        res = financeiro_client.delete(DETAIL_URL(pk))
        assert res.status_code == 204
        assert not Customer.objects.filter(pk=pk).exists()
        assert Customer.dm_objects.filter(pk=pk).exists()


@pytest.mark.django_db
class TestCustomerViewsFiltros:

    def test_busca_por_nome(self, admin_client, db):
        CustomerFactory(name='Zacarias Provedor')
        CustomerFactory(name='Maria Cliente')
        res = admin_client.get(LIST_URL, {'search': 'Zacarias'})
        assert res.status_code == 200
        assert res.data['count'] == 1

    def test_busca_por_cpf(self, admin_client, db):
        CustomerFactory(cpf='52998224725')
        CustomerFactory(cpf='')
        res = admin_client.get(LIST_URL, {'search': '529'})
        assert res.status_code == 200
        assert res.data['count'] == 1

    def test_paginacao(self, admin_client, db):
        CustomerFactory.create_batch(25)
        res = admin_client.get(LIST_URL)
        assert res.status_code == 200
        assert 'next' in res.data
        assert len(res.data['results']) == 20  # page_size padrão
