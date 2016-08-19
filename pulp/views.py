from pulp import models, serializers

import json
import django_filters
from rest_framework import filters, routers, viewsets


class RepositoryFilter(filters.FilterSet):
    repo__in = django_filters.MethodFilter(action='in_list_filter')

    class Meta:
        model = models.Repository
        fields = ['slug', 'repo__in']

    def in_list_filter(self, queryset, value):
        value = json.loads(value)
        return queryset.filter(slug__in=value)


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
