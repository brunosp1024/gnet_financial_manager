from rest_framework.routers import DefaultRouter
from django.urls import path
from .transaction_views import TransactionViewSet

router = DefaultRouter()
router.register(r'finance/transactions', TransactionViewSet, basename='finance-transactions')

dashboard = TransactionViewSet.as_view({'get': 'dashboard'})

urlpatterns = [
	path('finance/dashboard/', dashboard, name='finance-dashboard'),
] + router.urls