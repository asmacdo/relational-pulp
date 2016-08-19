from pulp.views import ContentUnitViewSet, CharInFilter, router
from pulp import models as pulp_models
from pulp_rpm import models, serializers

from rest_framework import filters


# class RPMFilter(filters.FilterSet):
#     """
#     """
#     # in_repo = CharInFilter(name='repositories', lookup_expr='in')

#     class Meta:
#         model = models.RPM
#         fields = ['repositories']


# TODO: Magic trick: autogenerate viewsets by finding contentunit model classes
class RPMViewSet(ContentUnitViewSet):
    queryset = models.RPM.objects.all()
    serializer_class = serializers.RPMSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('name',)
    # filter_class = RPMFilter


class SRPMViewSet(ContentUnitViewSet):
    """This is a test!

    Check out the SRPM API endpoint to see it render this docstring.
    """
    queryset = models.SRPM.objects.all()
    serializer_class = serializers.SRPMSerializer

router.register(r'content/rpm', RPMViewSet)
router.register(r'content/srpm', SRPMViewSet)
