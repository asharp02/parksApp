from whereToPark.models import ByLaw, Intersection, Highway
from rest_framework import serializers


class HighwaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Highway
        fields = ["name"]
        read_only_fields = fields


class IntersectionSerializer(serializers.ModelSerializer):
    main_street = HighwaySerializer(read_only=True)
    cross_street = HighwaySerializer(read_only=True)

    class Meta:
        model = Intersection
        fields = ["main_street", "cross_street", "lat", "lng"]
        read_only_fields = fields


class ByLawSerializer(serializers.Serializer):
    boundary_start = IntersectionSerializer(read_only=True)
    boundary_end = IntersectionSerializer(read_only=True)
    midpoint = serializers.ReadOnlyField()
    highway = HighwaySerializer(read_only=True)
    source_id = serializers.IntegerField(read_only=True)
    schedule = serializers.CharField(read_only=True)
    schedule_name = serializers.CharField(read_only=True)
    side = serializers.CharField(read_only=True)
    between = serializers.CharField(read_only=True)
    times_and_or_days = serializers.CharField(read_only=True)
    max_period_permitted = serializers.CharField(read_only=True)

    class Meta:
        model = ByLaw
