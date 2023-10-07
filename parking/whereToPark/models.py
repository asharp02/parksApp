from django.db import models


STREET_SIDES = (("W", "West"), ("E", "East"), ("N", "North"), ("S", "South"))
BOUNDARY_STATUSES = (
    ("NA", "Not Attempted"),
    ("FS", "Fetched Success"),
    ("FNF", "Fetched not found"),
    ("TO", "Timed out"),
)


class Intersection(models.Model):
    main_street = models.ForeignKey("Highway", on_delete=models.CASCADE)
    cross_street = models.ForeignKey("Highway", on_delete=models.CASCADE)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)
    status = models.CharField(choices=BOUNDARY_STATUSES, max_length=3, default="NA")


class ByLaw(models.Model):
    """Abstract base model class used in both NoParking and RestrictedParking
    models. This allows us to share fields across models and setting it to be
    abstract ensures a DB table is not created.
    """

    schedule = models.CharField(max_length=10)
    schedule_name = models.CharField(max_length=100)
    highway = models.ForeignKey("Highway", on_delete=models.CASCADE)
    side = models.CharField(max_length=10, null=True)
    boundary_start = models.ForeignKey("Intersection", on_delete=models.CASCADE)
    boundary_end = models.ForeignKey("Intersection", on_delete=models.CASCADE)
    between = models.CharField(max_length=200, null=True)

    class Meta:
        abstract = True


class NoParkingByLaw(ByLaw):
    """
    This model represents the "No Parking" dataset provided by the city of Toronto". Each
    record will represent a bylaw that specifies where and when you can't park.
    """

    source_id = models.IntegerField(unique=True)
    prohibited_times_and_or_days = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"{self.highway} ({self.side}) - {self.source_id}"


class RestrictedParkingByLaw(ByLaw):
    """
    This model represents the "Restricted Parking" dataset provided by the city of Toronto. Each
    record will represent a bylaw that specifies when/where someone is allowed to park and for
    how long.
    """

    source_id = models.IntegerField(unique=True)
    times_and_or_days = models.CharField(max_length=200, null=True)
    max_period_permitted = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.highway} ({self.side}) - {self.source_id}"


class Highway(models.Model):
    name = models.CharField(max_length=100)
    street_end = models.CharField(choices=STREET_SIDES, max_length=10, null=True)

    class Meta:
        unique_together = ["name", "street_end"]

    def __str__(self):
        return f"{self.name} {self.street_end}" if self.street_end else self.name
