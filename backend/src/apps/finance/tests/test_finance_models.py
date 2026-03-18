from datetime import datetime
from django.utils import timezone

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
    
    def test_transaction_factory_naive_datetime(self):
        naive_dt = datetime(2024, 3, 18, 10, 0, 0)  # Sem timezone
        tx = TransactionFactory(created_at=naive_dt)
        assert timezone.is_aware(tx.created_at)
