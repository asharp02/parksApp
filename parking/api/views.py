from geopy import distance

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import generics
from rest_framework import permissions
from api.serializers import (
    ByLawSerializer,
    HighwaySerializer,
    IntersectionSerializer,
)
from whereToPark.models import ByLaw
from django.db.models import Q


class BoundingBoxFilterBackend(filters.BaseFilterBackend):

    def get_box_from_center(self, lat, lng):
        """
        Takes in lat and lng of center on map.
        Returns list of four coordinates (tuples) representing the box from given center:
        [(NE_LAT, NE_LNG), (SW_LAT, SW_LNG)]
        """
        ne_point = distance.distance(kilometers=2).destination((lat, lng), bearing=45)
        sw_point = distance.distance(kilometers=2).destination((lat, lng), bearing=225)
        return [ne_point, sw_point]

    def get_box_q_obj(self, box):
        """
        Given NE and SW points X kms from center point, return Q object
        to filter ByLaws by these two points (ie. contained within X kms radius).

        ``box`` - list of two ``geopy.point.Point``, NE and SW points
        """
        min_lat = box[1].latitude
        min_lng = box[1].longitude
        max_lat = box[0].latitude
        max_lng = box[0].longitude

        # Filter won't be exact since we attempt to match either ``boundary_start`` or ``boundary_end``
        # intersections rather than the midpoint (cached property on model, not filterable)
        start_q = Q(
            boundary_start__lat__gte=min_lat,
            boundary_start__lat__lte=max_lat,
            boundary_start__lng__gte=min_lng,
            boundary_start__lng__lte=max_lng,
        )
        end_q = Q(
            boundary_end__lat__gte=min_lat,
            boundary_end__lat__lte=max_lat,
            boundary_end__lng__gte=min_lng,
            boundary_end__lng__lte=max_lng,
        )

        return start_q | end_q

    def filter_queryset(self, request, queryset, view):
        lat = request.query_params.get("lat")
        lng = request.query_params.get("lng")
        filter_qs = Q()
        if lat and lng:
            bounding_box = self.get_box_from_center(lat, lng)
            filter_qs = self.get_box_q_obj(bounding_box)

        return queryset.filter(filter_qs)


class TypeFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        bylaw_type = request.query_params.get("type")
        if not bylaw_type:
            return queryset

        if bylaw_type == "np":
            return queryset.filter(schedule="13")
        else:
            return queryset.filter(schedule="15")


class ByLawViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that No Parking Bylaws to be viewed.
    """

    queryset = ByLaw.objects.get_bylaws_to_display().order_by("source_id")
    serializer_class = ByLawSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [BoundingBoxFilterBackend, TypeFilterBackend]
