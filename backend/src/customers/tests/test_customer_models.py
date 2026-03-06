import pytest
from customers.tests.factories import CustomerFactory


@pytest.mark.django_db
class TestCustomerModel:

    def test_cria_cliente(self):
        c = CustomerFactory(name='Empresa X')
        assert c.pk is not None
        assert c.name == 'Empresa X'

    def test_str_retorna_nome(self):
        c = CustomerFactory(name='João')
        assert str(c) == 'João'
