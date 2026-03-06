import pytest
from rest_framework.test import APIRequestFactory
from finance.serializers import TransactionSerializer
from finance.tests.factories import TransactionFactory
from customers.tests.factories import CustomerFactory


def make_request(user):
    f = APIRequestFactory()
    req = f.post('/')
    req.user = user
    return req


@pytest.mark.django_db
class TestTransactionSerializer:

    def test_campos_read_only(self, admin_user):
        data = {
            'type':        'INCOME',
            'category':    'MONTHLY_FEE',
            'value':       '100.00',
            'payment_method': 'PIX',
            'created_by':  str(admin_user.pk),  # Should be ignored
        }
        ts = TransactionSerializer(data=data, context={'request': make_request(admin_user)})
        assert ts.is_valid(), ts.errors
        t = ts.save()
        assert t.created_by == admin_user

    def test_customer_name_read_only(self):
        t = TransactionFactory()
        s = TransactionSerializer(t)
        assert s.data['customer_name'] == t.customer.name
