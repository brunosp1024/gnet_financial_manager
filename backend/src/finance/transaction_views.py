
from datetime import date
from django.db.models import Count, Sum
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from .models import Transaction
from .serializers import TransactionSerializer


class TransactionViewSet(ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    search_fields = ['description']
    ordering_fields = ['value', 'category', 'type', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = Transaction.objects.select_related('created_by', 'updated_by')
        p  = self.request.query_params
        
        if p.get('type'): qs = qs.filter(type=p['type'])
        if p.get('category'): qs = qs.filter(category=p['category'])
        if p.get('date_from'): qs = qs.filter(created_at__gte=p['date_from'])
        if p.get('date_to'): qs = qs.filter(created_at__lte=p['date_to'])

        return qs
    
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
            'transactions': TransactionSerializer(qs, many=True).data,
            'total_income': float(inc),
            'total_expense': float(exp),
            'balance': float(inc - exp),
        })
