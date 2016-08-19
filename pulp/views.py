from pulp import models, serializers

import json
from rest_framework import filters, routers, viewsets


class JSONFilterViewSet(viewsets.ModelViewSet):
    """
    Allows ViewSet writer to explicitly allow lookup expressions that require JSON parsing.
    """
    whitelist_json_filters = []

    def get_queryset(self):
        qs = self.queryset
        for key, value in self.request.query_params.items():
            if key in self.whitelist_json_filters:
                qs_filter = {key: json.loads(value)}
                qs = qs.filter(**qs_filter)
        return qs


class RepositoryViewSet(JSONFilterViewSet):
    whitelist_json_filters = ['slug__in']
    lookup_field = 'slug'
    queryset = models.Repository.objects.all()
    serializer_class = serializers.RepositorySerializer
    filter_backends = (filters.DjangoFilterBackend,)


# XXX DO NOT register ContentUnitViewSet with the router.
# It's here to be subclasses by the specific unit types,
# not to provide its own views. *Always* drive unit API
# views to the specific type.
class ContentUnitViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ContentUnitSerializer

router = routers.DefaultRouter()
router.register(r'repositories', RepositoryViewSet)
