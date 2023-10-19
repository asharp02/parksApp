from django.db import models
from django.db.models import Q
from django.utils.functional import cached_property


STREET_SIDES = (("W", "West"), ("E", "East"), ("N", "North"), ("S", "South"))
BOUNDARY_STATUSES = (
    ("NA", "Not Attempted"),
    ("FS", "Fetched Success"),
    ("FNF", "Fetched not found"),
    ("TO", "Timed out"),
)


class Intersection(models.Model):
    main_street = models.ForeignKey(
        "Highway", on_delete=models.CASCADE, related_name="main_street", null=True
    )
    cross_street = models.ForeignKey(
        "Highway", on_delete=models.CASCADE, related_name="cross_street", null=True
    )
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)
    status = models.CharField(choices=BOUNDARY_STATUSES, max_length=3, default="NA")

    def __str__(self):
        return f"{self.main_street} at {self.cross_street} ({self.status})"

    class Meta:
        unique_together = ["main_street", "cross_street"]


class ByLawManager(models.Manager):
    related_objs = [
        "boundary_start",
        "boundary_end",
        "boundary_start__main_street",
        "boundary_start__cross_street",
        "boundary_end__main_street",
        "boundary_end__cross_street",
    ]

    def get_np_bylaws_to_display(self):
        return (
            self.filter(schedule="13")
            .filter(boundary_start__status="FS", boundary_end__status="FS")
            .select_related(*self.related_objs)
        )

    def get_rp_bylaws_to_display(self):
        return (
            self.filter(schedule="15")
            .filter(boundary_start__status="FS", boundary_end__status="FS")
            .select_related(*self.related_objs)
        )

    def get_bylaws_to_update(self):
        """
        query to get all bylaws whose locations (boundary_start and boundary_end) need updating.
        We only need to update bylaws with boundaries that have not been attempted yet (ie status
        is 'NA' or 'TO')
        """
        exclude_qs = Q(boundary_start=None) | Q(boundary_end=None)

        filter_qs = Q(boundary_start__status__in=["NA", "TO"]) | Q(
            boundary_end__status__in=["NA", "TO"]
        )
        return (
            self.exclude(exclude_qs)
            .filter(filter_qs)
            .select_related(*self.related_objs)
        )


class ByLaw(models.Model):
    """
    Model used to represent both No Parking and Restricted Parking bylaws.
    """

    source_id = models.IntegerField(null=True)
    schedule = models.CharField(max_length=10)
    schedule_name = models.CharField(max_length=100)
    highway = models.ForeignKey("Highway", on_delete=models.CASCADE)
    side = models.CharField(max_length=10, null=True)
    boundary_start = models.ForeignKey(
        "Intersection",
        on_delete=models.CASCADE,
        related_name="boundary_start",
        null=True,
    )
    boundary_end = models.ForeignKey(
        "Intersection", on_delete=models.CASCADE, related_name="boundary_end", null=True
    )
    between = models.CharField(max_length=200, null=True)
    times_and_or_days = models.CharField(
        max_length=200, null=True
    )  # represents prohibited times/days if a No Parking bylaw or allowed times/days if restricted parking
    max_period_permitted = models.CharField(
        max_length=100, null=True
    )  # only set for restricted parking
    objects = ByLawManager()

    def __str__(self):
        return f"{self.highway} ({self.side}) - {self.source_id}"

    @cached_property
    def midpoint(self):
        if not self.boundary_start or not self.boundary_end:
            return (None, None)
        lat_mid = (self.boundary_start.lat + self.boundary_end.lat) / 2
        lng_mid = (self.boundary_start.lng + self.boundary_end.lng) / 2
        return (lat_mid, lng_mid)

    @cached_property
    def popup_html(self):
        html = f"<h1>ByLaw</h1><br/><h3>{self.highway} at {self.between}</h3>"
        print(html)
        return html

    class Meta:
        unique_together = ["schedule", "source_id"]


class Highway(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
