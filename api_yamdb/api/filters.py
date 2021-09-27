import django_filters

from .models import Title


class TitlesFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(
        field_name='genre__slug',
        lookup_expr='contains'
    )
    category = django_filters.CharFilter(
        field_name='category__slug',
        lookup_expr='contains'
    )
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='contains'
    )

    class Meta:
        model = Title
        fields = ('genre', 'category', 'year')
