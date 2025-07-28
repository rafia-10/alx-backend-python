import django_filters
from .models import message

class MessageFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='timestamp', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='timestamp', lookup_expr='lte')
    sender = django_filters.CharFilter(field_name='sender__username', lookup_expr='iexact')

    class Meta:
        model = message
        fields = ['start_date', 'end_date', 'sender']