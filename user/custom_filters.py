from django_filters import FilterSet, CharFilter, OrderingFilter

class UserFilter(FilterSet):
    email = CharFilter(lookup_expr='icontains')
    username = CharFilter(lookup_expr='icontains')
    order_by = OrderingFilter(
        fields=(
            ('email', 'email'),
            ('username', 'username'),
        )
    )
    @property
    def qs(self):
        return super().qs
