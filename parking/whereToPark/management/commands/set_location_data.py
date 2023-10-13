from urllib3.util import Retry
from requests import Session
import time
from requests.exceptions import RetryError
from requests.adapters import HTTPAdapter
from xml.etree import ElementTree as ET
from decimal import Decimal

from django.db.models import Q
from django.core.management.base import BaseCommand, CommandError

from whereToPark.models import ByLaw, Intersection, Highway

GEOCODER_API_ENDPOINT = "https://geocoder.ca/"
URL_PARAMS = "&city=toronto&geoit=xml"


class Command(BaseCommand):
    intersections_to_update = []
    timeout_count = 0

    def handle(self, *args, **options):
        self.import_intersections()
        self.set_intersections_with_loc()
        update_fields = ["status", "lat", "lng"]
        Intersection.objects.bulk_update(self.intersections_to_update, update_fields)

    def set_intersections_with_loc(self):
        exclude_q = (
            Q(boundary_start__status__in=["FS", "FNF"])
            | Q(boundary_end__status__in=["FS", "FNF"])
            | Q(boundary_start=None)
            | Q(boundary_end=None)
        )
        for bylaw in ByLaw.objects.exclude(exclude_q)[:5]:
            self.set_boundaries(bylaw)
            if self.timeout_count >= 5:
                break

    def set_boundaries(self, law):
        for intersection in [law.boundary_start, law.boundary_end]:
            (lat, lng), status = self.fetch_geocode(intersection)
            if lat and lng:
                intersection.lat = lat
                intersection.lng = lng
                intersection.status = status
                self.intersections_to_update.append(intersection)

    def fetch_geocode(self, intersection):
        """Handles calling the geocoder API endpoint to fetch lat/lng data
        for the highway (road) and cross street given. Currently uses the free tier which
        is heavily throttled"""
        highway = intersection.main_street.name
        cross_street = intersection.cross_street.name
        if not highway or not cross_street:
            return (None, None), "FNF"
        print(f"fetching {highway} at {cross_street}")
        url = f"{GEOCODER_API_ENDPOINT}?street1={highway}&street2={cross_street}{URL_PARAMS}"
        try:
            s = Session()
            retries = Retry(
                total=5,
                backoff_factor=1,
                status_forcelist=[403],
                allowed_methods=["GET"],
            )
            s.mount("https://", HTTPAdapter(max_retries=retries))
            resp = s.get(url)
        except RetryError as err:
            print(f"Fetching geocode for {highway} at {cross_street} failed: {err}")
        else:
            tree = ET.fromstring(resp.content)
            return self.parse_geocode_xml(tree)
        self.timeout_count += 1
        print(f"Timed out on {highway} at {cross_street}, gave up")
        return (None, None), "TO"

    def parse_geocode_xml(self, tree):
        """Given an element tree with XML from geocoder API, parse latitude and longitude
        fields.
        """
        lat, lng = None, None
        confidence_score = 0
        for child in tree:
            if child.tag == "error":
                return (None, None), "TO"
            if child.tag == "latt" and child.text:
                lat = float(child.text)
            elif child.tag == "longt" and child.text:
                lng = float(child.text)
            elif child.tag == "confidence" and child.text:
                confidence_score = child.text

        if float(confidence_score) < 0.5:
            print("Geocode for intersection not found")
            return (None, None), "FNF"
        return (lat, lng), "FS"

    def parse_between_field(self, between):
        if not between:
            return None, None
        cross_streets = between.split(" and ")
        if len(cross_streets) != 2:
            return None, None
        cross_highway_a = Highway.objects.filter(name=cross_streets[0]).first()
        cross_highway_b = Highway.objects.filter(name=cross_streets[1]).first()
        return cross_highway_a, cross_highway_b

    def import_intersections(self):
        bylaws_to_update = []
        for bylaw in ByLaw.objects.all():
            cross_highway_a, cross_highway_b = self.parse_between_field(bylaw.between)
            if not cross_highway_a or not cross_highway_b:
                continue
            main_highway = bylaw.highway
            intersection_start, _ = Intersection.objects.get_or_create(
                main_street=main_highway, cross_street=cross_highway_a
            )
            intersection_end, _ = Intersection.objects.get_or_create(
                main_street=main_highway, cross_street=cross_highway_b
            )
            bylaw.boundary_start = intersection_start
            bylaw.boundary_end = intersection_end
            bylaws_to_update.append(bylaw)
        ByLaw.objects.bulk_update(bylaws_to_update, ["boundary_start", "boundary_end"])
