from django.db import models


STREET_SIDES = (("W", "West"), ("E", "East"), ("N", "North"), ("S", "South"))


# Create your models here.
class ParkingByLaw(models.Model):
    """
    This model represents two datasets provided by City of Toronto: "No Parking"
    and "Parking for Restricted Periods". Each record will represent a bylaw
    that specifies either the time range/location of where someone can or cant park.
    """

    bylaw_no = models.CharField(max_length=100)
    source_id = models.CharField(max_length=10)
    schedule = models.CharField(max_length=10)
    schedule_name = models.CharField(max_length=100)
    highway = models.CharField(max_length=100)
    side = models.CharField(max_length=10)
    between = models.CharField(max_length=200)
    times_and_or_days = models.CharField(max_length=200)
    max_period_permitted = models.CharField(max_length=100)
