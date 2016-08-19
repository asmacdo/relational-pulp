from pulp import models, serializers

import django_filters
from rest_framework import filters
from rest_framework import routers, viewsets


class CharInFilter(django_filters.filters.BaseInFilter,
                   django_filters.filters.CharFilter):
    pass


class RepositoryFilter(filters.FilterSet):
    """
    Allows this search:
    http 'http://example/api/v3/repositories/?slug_in_list=singing-gerbil,versatile-pudu'
    """

    # Potential 'gotcha' here: This field cannot be called "slug__in" because django_filters
    # recognizes this as special syntax and tries to do its own stuff to it. (I think it looks for
    # and `in` sub-field within the slug field.
    slug_in_list = CharInFilter(name='slug', lookup_expr='in')

    class Meta:
        model = models.Repository
        fields = ['slug_in_list']


class RepositoryViewSet(viewsets.ModelViewSet):
    lookup_field = 'slug'
    queryset = models.Repository.objects.all()
    serializer_class = serializers.RepositorySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = RepositoryFilter


# XXX DO NOT register ContentUnitViewSet with the router.
# It's here to be subclasses by the specific unit types,
# not to provide its own views. *Always* drive unit API
# views to the specific type.
class ContentUnitViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ContentUnitSerializer

router = routers.DefaultRouter()
router.register(r'repositories', RepositoryViewSet)
