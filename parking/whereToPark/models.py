from django.db import models


STREET_SIDES = (("W", "West"), ("E", "East"), ("N", "North"), ("S", "South"))


# Create your models here.
class NoParkingByLaw(models.Model):
    """
    This model represents "No Parking" dataset provided by the city of Toronto". Each
    record will represent a bylaw that specifies when/where someone can park and for how long.
    """

    bylaw_no = models.CharField(max_length=100)
    source_id = models.CharField(max_length=10)
    schedule = models.CharField(max_length=10)
    schedule_name = models.CharField(max_length=100)
    highway = models.CharField(max_length=100)
    side = models.CharField(max_length=10)
    between = models.CharField(max_length=200)
    times_and_or_days = models.CharField(max_length=200)
    prohibited_times_and_or_days = models.CharField(max_length=100)


class RestrictedParkingByLaw(models.Model):
    """
    This model represents the "Restricted Parking" dataset provided by the city of Toronto. Each
    record will represent a bylaw that specifies when/where someone is restricted from parking
    and for how long.
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
