from whereToPark.models import ByLaw, Intersection, Highway
from rest_framework import serializers


class HighwaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Highway
        fields = ["name"]


class IntersectionSerializer(serializers.ModelSerializer):
    main_street = HighwaySerializer(read_only=True)
    cross_street = HighwaySerializer(read_only=True)

    class Meta:
        model = Intersection
        fields = ["main_street", "cross_street", "lat", "lng"]


class ByLawSerializer(serializers.ModelSerializer):
    boundary_start = IntersectionSerializer(read_only=True)
    boundary_end = IntersectionSerializer(read_only=True)
    midpoint = serializers.ReadOnlyField()
    highway = HighwaySerializer(read_only=True)

    class Meta:
        model = ByLaw
        fields = [
            "source_id",
            "schedule",
            "schedule_name",
            "highway",
            "side",
            "boundary_start",
            "boundary_end",
            "between",
            "times_and_or_days",
            "max_period_permitted",
            "midpoint",
        ]
