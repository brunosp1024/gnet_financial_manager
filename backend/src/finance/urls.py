from rest_framework.routers import DefaultRouter
from django.urls import path
from .transaction_views import TransactionViewSet
from .dashboard_views import FinanceDashboardView

router = DefaultRouter()
router.register(r'finance/transactions', TransactionViewSet, basename='finance-transactions')

urlpatterns = [
	path('finance/dashboard/', FinanceDashboardView.as_view(), name='finance-dashboard'),
] + router.urls