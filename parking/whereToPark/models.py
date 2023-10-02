from django.db import models


STREET_SIDES = (("W", "West"), ("E", "East"), ("N", "North"), ("S", "South"))


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
    prohibited_times_and_or_days = models.CharField(max_length=200, null=True)
    boundary_a_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    boundary_a_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    boundary_b_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    boundary_b_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True)

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
    times_and_or_days = models.CharField(max_length=200, null=True)
    max_period_permitted = models.CharField(max_length=100, null=True)
    boundary_a_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    boundary_a_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    boundary_b_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    boundary_b_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True)

    def __str__(self):
        return f"{self.highway} ({self.side}) - {self.source_id}"
