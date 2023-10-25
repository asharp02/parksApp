from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from api.serializers import (
    ByLawSerializer,
    HighwaySerializer,
    IntersectionSerializer,
)
from whereToPark.models import ByLaw


class NPByLawViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that No Parking Bylaws to be viewed.
    """

    queryset = ByLaw.objects.get_np_bylaws_to_display().order_by("source_id")
    serializer_class = ByLawSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class RPByLawViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that Restricted Parking Bylaws to be viewed.
    """

    queryset = ByLaw.objects.get_rp_bylaws_to_display().order_by("source_id")
    serializer_class = ByLawSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
