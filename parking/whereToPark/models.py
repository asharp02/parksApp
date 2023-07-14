from django.db import models


STREET_SIDES = (("W", "West"), ("E", "East"), ("N", "North"), ("S", "South"))


# Create your models here.
# class ParkingByLaws(models.Model):
#     """
#     This model represents two datasets provided by City of Toronto: "No Parking"
#     and "Parking for Restricted Periods". Each record will represent a bylaw
#     that specifies either the time range/location of where someone can or cant park.
#     """

#     id = models.IntegerField()
#     side_of_road = models.CharField(max_length=10, choices=STREET_SIDES)
#     road_name = models.CharField(max_length=100)
#     boundaries = models.CharField(max_length=100)  # Consider using long/lat values
#     times_specified = models.CharField(
#         max_length=100
#     )  # range representing parking period
#     can_park = models.BooleanField()
#     max_period_permitted = models.PositiveSmallIntegerField()  # in hours
