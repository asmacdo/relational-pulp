from pulp import models, serializers

import django_filters
from rest_framework import filters
from rest_framework import routers, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from pulp_rpm import models as rpm_models
from pulp_rpm import serializers as rpm_serializers


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

    @detail_route(methods=['GET'])
    def associations(self, request, slug=None):
        units_in_repo = rpm_models.RPM.objects.filter(repositories__slug=slug)
        serializer = rpm_serializers.RPMSerializer(units_in_repo, context={'request': request})
        return Response(serializer.data)

    # def recent_users(self, request):
    #     recent_users = User.objects.all().order('-last_login')

    #     page = self.paginate_queryset(recent_users)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)

    #     serializer = self.get_serializer(recent_users, many=True)
    #     return Response(serializer.data)


# XXX DO NOT register ContentUnitViewSet with the router.
# It's here to be subclasses by the specific unit types,
# not to provide its own views. *Always* drive unit API
# views to the specific type.
class ContentUnitViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ContentUnitSerializer

router = routers.DefaultRouter()
router.register(r'repositories', RepositoryViewSet)
