import pytest
from apps.finance.models import Transaction
from apps.finance.tests.factories import TransactionFactory


@pytest.mark.django_db
class TestTransactionModel:

    def test_create_transaction(self):
        t = TransactionFactory(value=99.90)
        assert t.pk is not None
        assert float(t.value) == 99.90

    def test_type_choices(self):
        income  = TransactionFactory(type=Transaction.Type.INCOME)
        expense = TransactionFactory(type=Transaction.Type.EXPENSE)
        assert income.type  == 'INCOME'
        assert expense.type == 'EXPENSE'
