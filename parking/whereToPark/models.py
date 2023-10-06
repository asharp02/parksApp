from django.db import models


STREET_SIDES = (("W", "West"), ("E", "East"), ("N", "North"), ("S", "South"))
BOUNDARY_STATUSES = (
    ("NA", "Not Attempted"),
    ("FS", "Fetched Success"),
    ("FNF", "Fetched not found"),
    ("TO", "Timed out"),
)


# Create your models here.
class NoParkingByLaw(models.Model):
    """
    This model represents "No Parking" dataset provided by the city of Toronto". Each
    record will represent a bylaw that specifies when/where someone can park and for how long.
    """

    bylaw_no = models.CharField(max_length=100)
    source_id = models.IntegerField(unique=True)
    schedule = models.CharField(max_length=10)
    schedule_name = models.CharField(max_length=100)
    highway = models.CharField(max_length=100)
    side = models.CharField(max_length=10, null=True)
    between = models.CharField(max_length=200, null=True)
    cross_street_a = models.CharField(max_length=200, null=True)
    cross_street_b = models.CharField(max_length=200, null=True)
    prohibited_times_and_or_days = models.CharField(max_length=200, null=True)
    boundary_a_lat = models.FloatField(null=True)
    boundary_a_lng = models.FloatField(null=True)
    boundary_b_lat = models.FloatField(null=True)
    boundary_b_lng = models.FloatField(null=True)
    boundary_status_a = models.CharField(
        choices=BOUNDARY_STATUSES, max_length=30, default="NA"
    )
    boundary_status_b = models.CharField(
        choices=BOUNDARY_STATUSES, max_length=30, default="NA"
    )

    def __str__(self):
        return f"{self.highway} ({self.side}) - {self.source_id}"


class RestrictedParkingByLaw(models.Model):
    """
    This model represents the "Restricted Parking" dataset provided by the city of Toronto. Each
    record will represent a bylaw that specifies when/where someone is restricted from parking
    and for how long.
    """

    bylaw_no = models.CharField(max_length=100)
    source_id = models.IntegerField(unique=True)
    schedule = models.CharField(max_length=10)
    schedule_name = models.CharField(max_length=100)
    highway = models.CharField(max_length=100)
    side = models.CharField(max_length=10, null=True)
    between = models.CharField(max_length=200, null=True)
    cross_street_a = models.CharField(max_length=200, null=True)
    cross_street_b = models.CharField(max_length=200, null=True)
    times_and_or_days = models.CharField(max_length=200, null=True)
    max_period_permitted = models.CharField(max_length=100, null=True)
    boundary_a_lat = models.FloatField(null=True)
    boundary_a_lng = models.FloatField(null=True)
    boundary_b_lat = models.FloatField(null=True)
    boundary_b_lng = models.FloatField(null=True)
    boundary_status_a = models.CharField(
        choices=BOUNDARY_STATUSES, max_length=30, default="NA"
    )
    boundary_status_b = models.CharField(
        choices=BOUNDARY_STATUSES, max_length=30, default="NA"
    )

    def __str__(self):
        return f"{self.highway} ({self.side}) - {self.source_id}"


class Highway(models.Model):
    name = models.CharField(max_length=100)
    street_end = models.CharField(choices=STREET_SIDES, max_length=10, null=True)

    class Meta:
        unique_together = ["name", "street_end"]

    def __str__(self):
        return f"{self.name} {self.street_end}" if self.street_end else self.name
