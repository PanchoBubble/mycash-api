from django_filters import FilterSet, CharFilter, OrderingFilter

class CurrencyFilter(FilterSet):
    code = CharFilter(lookup_expr='icontains')
    name = CharFilter(lookup_expr='icontains')
    order_by = OrderingFilter(
        fields=(
            ('code', 'code'),
            ('name', 'name'),
        )
    )
    @property
    def qs(self):
        return super().qs

class StockFilter(FilterSet):
    currency = CharFilter(field_name='currency__code',lookup_expr='icontains')
    owner = CharFilter(field_name='owner__username',lookup_expr='icontains')
    amount = CharFilter(lookup_expr='icontains')
    order_by = OrderingFilter(
        fields=(
            ('currency__code', 'currency'),
            ('owner__username', 'owner'),
            ('ammount', 'ammount'),
        )
    )
    @property
    def qs(self):
        # The query context can be found in self.request.
        return super().qs