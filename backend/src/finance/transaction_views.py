
from datetime import date
from django.db.models import Count, Sum
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from core.permissions import GroupPermission
from .models import Transaction
from .serializers import (
    TransactionCreateSerializer,
    TransactionUpdateSerializer,
    TransactionListSerializer,
    TransactionDetailSerializer,
)


class TransactionViewSet(ModelViewSet):
    serializer_class = TransactionListSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    search_fields = ['description']
    ordering_fields = ['value', 'category', 'type', 'created_at']
    ordering = ['-created_at']
    serializer_classes = {
        'create': TransactionCreateSerializer,
        'list': TransactionListSerializer,
        'retrieve': TransactionDetailSerializer,
        'update': TransactionUpdateSerializer,
        'partial_update': TransactionUpdateSerializer,
    }

    def get_queryset(self):
        qs = Transaction.objects.select_related('created_by', 'updated_by')
        qp  = self.request.query_params
        if qp.get('type'):
            qs = qs.filter(type=qp['type'])
        if qp.get('category'):
            qs = qs.filter(category=qp['category'])
        if qp.get('date_from'):
            qs = qs.filter(created_at__date__gte=qp['date_from'])
        if qp.get('date_to'):
            qs = qs.filter(created_at__date__lte=qp['date_to'])

        return qs

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        qs  = self.get_queryset()
        inc = qs.filter(type='INCOME').aggregate(t=Sum('value'))['t'] or 0
        exp = qs.filter(type='EXPENSE').aggregate(t=Sum('value'))['t'] or 0

        by_category = (
            qs.values('category', 'type')
              .annotate(total=Sum('value'), count=Count('id'))
              .order_by('-total')
        )

        return Response({
            'income_total': float(inc),
            'expense_total': float(exp),
            'balance': float(inc - exp),
            'transaction_count': qs.count(),
            'by_category': list(by_category),
        })

    @action(detail=False, methods=['get'])
    def daily_report(self, request):
        today = date.today()
        qs = Transaction.objects.filter(created_at__date=today)
        inc = qs.filter(type='INCOME').aggregate(t=Sum('value'))['t']  or 0
        exp = qs.filter(type='EXPENSE').aggregate(t=Sum('value'))['t'] or 0

        return Response({
            'date': str(today),
            'transactions': TransactionListSerializer(qs, many=True).data,
            'total_income': float(inc),
            'total_expense': float(exp),
            'balance': float(inc - exp),
        })
