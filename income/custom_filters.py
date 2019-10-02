from django_filters import FilterSet, CharFilter, OrderingFilter

class IncomeFilter(FilterSet):
    amount = CharFilter(lookup_expr='icontains')
    description = CharFilter(lookup_expr='icontains')
    owner = CharFilter(field_name="owner__username",lookup_expr='icontains')
    date = CharFilter(lookup_expr='icontains')
    order_by = OrderingFilter(
        fields=(
            ('amount', 'amount'),
            ('description', 'description'),
            ('owner', 'owner'),
            ('date', 'date'),
        )
    )
    # status=django_filters.BooleanFilter(field_name='status')
    @property
    def qs(self):
        # The query context can be found in self.request.
        return super().qs

class IncomeTypeFilter(FilterSet):
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