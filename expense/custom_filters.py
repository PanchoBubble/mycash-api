from django_filters import FilterSet, CharFilter, OrderingFilter

class ExpenseFilter(FilterSet):
    cost = CharFilter(lookup_expr='icontains')
    date = CharFilter(lookup_expr='icontains')
    description = CharFilter(lookup_expr='icontains')
    state = CharFilter(lookup_expr='icontains')
    owner = CharFilter(field_name="owner__username",lookup_expr='icontains')
    type = CharFilter(field_name="type__name",lookup_expr='icontains')
    currency = CharFilter(field_name="currency__code",lookup_expr='icontains')
    order_by = OrderingFilter(
        fields=(
            ('cost', 'cost'),
            ('description', 'description'),
            ('owner__username', 'owner'),
            ('date', 'date'),
            ('state', 'state'),
            ('currency__name', 'currency'),
            ('type__code', 'type'),
        )
    )
    @property
    def qs(self):
        return super().qs

class ExpenseTypeFilter(FilterSet):
    name = CharFilter(lookup_expr='icontains')
    description = CharFilter(lookup_expr='icontains')
    order_by = OrderingFilter(
        fields=(
            ('name', 'name'),
            ('description', 'description'),
        )
    )
    @property
    def qs(self):
        # The query context can be found in self.request.
        return super().qs