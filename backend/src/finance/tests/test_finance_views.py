import pytest
from datetime import date
from finance.tests.factories import TransactionFactory
from finance.models import Transaction
from customers.tests.factories import CustomerFactory

LIST_URL      = '/api/finance/transactions/'
REPORT_URL    = '/api/finance/transactions/daily_report/'
DASHBOARD_URL = '/api/finance/dashboard/'

def DETAIL_URL(pk):
    return f'/api/finance/transactions/{pk}/'

REPORT_URL    = '/api/finance/transactions/daily_report/'
DASHBOARD_URL = '/api/finance/dashboard/'


@pytest.mark.django_db
class TestTransactionViewsAuthentication:

    def test_without_token_returns_401(self, api_client):
        assert api_client.get(LIST_URL).status_code == 401

    def test_without_token_on_dashboard_returns_401(self, api_client):
        assert api_client.get(DASHBOARD_URL).status_code == 401


@pytest.mark.django_db
class TestTransactionViewsPermissions:

    def test_admin_can_list(self, admin_client):
        TransactionFactory.create_batch(3)
        response = admin_client.get(LIST_URL)
        assert response.status_code == 200

    def test_financeiro_can_list(self, financeiro_client):
        response = financeiro_client.get(LIST_URL)
        assert response.status_code == 200

    def test_financeiro_can_create(self, financeiro_client, db):
        customer = CustomerFactory()
        data = {
            'type':        'INCOME',
            'category':    'MONTHLY_FEE',
            'value':       '99.90',
            'payment_method': 'PIX',
            'customer_id': str(customer.pk),
        }
        response = financeiro_client.post(LIST_URL, data)
        assert response.status_code == 201

    def test_financeiro_can_soft_delete(self, financeiro_client, db):
        transaction = TransactionFactory()
        pk = transaction.pk
        response = financeiro_client.delete(DETAIL_URL(pk))
        assert response.status_code == 204
        assert not Transaction.objects.filter(pk=pk).exists()
        assert Transaction.dm_objects.filter(pk=pk).exists()


@pytest.mark.django_db
class TestTransactionViewsFilters:

    def test_filter_by_type(self, admin_client, db):
        TransactionFactory(type='INCOME')
        TransactionFactory(type='EXPENSE')
        response = admin_client.get(LIST_URL, {'type': 'INCOME'})
        assert response.status_code == 200
        assert all(item['type'] == 'INCOME' for item in response.data['results'])

    def test_filter_by_category(self, admin_client, db):
        TransactionFactory(category='MONTHLY_FEE')
        TransactionFactory(category='LOGISTIC')
        response = admin_client.get(LIST_URL, {'category': 'MONTHLY_FEE'})
        assert response.status_code == 200
        assert all(item['category'] == 'MONTHLY_FEE' for item in response.data['results'])

    def test_filter_by_date_range(self, admin_client, db):
        TransactionFactory(created_at=date(2024, 1, 15))
        TransactionFactory(created_at=date(2024, 6, 15))
        response = admin_client.get(LIST_URL, {
            'date_from': '2024-01-01',
            'date_to':   '2024-03-31',
        })
        assert response.status_code == 200
        assert response.data['count'] == 1


@pytest.mark.django_db
class TestDailyReport:

    def test_returns_only_today_transactions(self, admin_client, db):
        TransactionFactory()
        TransactionFactory()
        TransactionFactory(created_at=date(2020, 1, 1))
        response = admin_client.get(REPORT_URL)
        assert response.status_code == 200
        assert len(response.data['transactions']) == 2

    def test_calculates_totals_correctly(self, admin_client, db):
        TransactionFactory(type='INCOME',  value=200)
        TransactionFactory(type='INCOME',  value=100)
        TransactionFactory(type='EXPENSE', value=80)
        response = admin_client.get(REPORT_URL)
        assert response.status_code == 200
        assert response.data['total_income']  == 300.0
        assert response.data['total_expense'] == 80.0
        assert response.data['balance']       == 220.0

    def test_day_without_transactions(self, admin_client, db):
        response = admin_client.get(REPORT_URL)
        assert response.status_code == 200
        assert response.data['total_income']  == 0
        assert response.data['total_expense'] == 0
        assert response.data['balance']       == 0


@pytest.mark.django_db
class TestDashboard:

    def test_returns_expected_structure(self, admin_client, db):
        TransactionFactory.create_batch(3)
        response = admin_client.get(DASHBOARD_URL)
        assert response.status_code == 200
        assert 'income_total'      in response.data
        assert 'expense_total'     in response.data
        assert 'balance'           in response.data
        assert 'transaction_count' in response.data
        assert 'by_category'       in response.data

    def test_financeiro_can_access_dashboard(self, financeiro_client):
        response = financeiro_client.get(DASHBOARD_URL)
        assert response.status_code == 200

    def test_filter_by_date_range_on_dashboard(self, admin_client, db):
        TransactionFactory(type='INCOME', value=500, created_at=date(2024, 1, 10))
        TransactionFactory(type='INCOME', value=300, created_at=date(2024, 6, 10))
        response = admin_client.get(DASHBOARD_URL, {
            'date_from': '2024-01-01',
            'date_to':   '2024-03-31',
        })
        assert response.status_code == 200
        assert response.data['income_total'] == 500.0
