from urllib3.util import Retry
from requests import Session
import time
from requests.exceptions import RetryError
from requests.adapters import HTTPAdapter
from xml.etree import ElementTree as ET
from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError

from whereToPark.models import NoParkingByLaw, RestrictedParkingByLaw

GEOCODER_API_ENDPOINT = "https://geocoder.ca/"
URL_PARAMS = "&city=toronto&geoit=xml"


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.handle_no_parking_locations()
        self.handle_restricted_locations()

    def handle_no_parking_locations(self):
        # we want to avoid complex between values ie. "a point 5 metres from" or
        # the west end of X
        for law in NoParkingByLaw.objects.exclude(between__icontains="point").exclude(
            between__icontains="end"
        ):
            self.handle_setting_boundaries(law)

    def handle_restricted_locations(self):
        # we want to avoid complex between values ie. "a point 5 metres from" or
        # the west end of X
        for law in RestrictedParkingByLaw.objects.exclude(
            between__icontains="point"
        ).exclude(between__icontains="end"):
            self.handle_setting_boundaries(law)

    def handle_between_field(self, law):
        return law.between.split(" and ")

    def handle_setting_boundaries(self, law):
        lat_a, lng_a = self.fetch_geocode(law.highway, law.cross_street_a)
        if lat_a and lng_a:
            law.boundary_a_lat = lat_a
            law.boundary_a_lng = lng_a
        lat_b, lng_b = self.fetch_geocode(law.highway, law.cross_street_b)
        if lat_b and lng_b:
            law.boundary_b_lat = lat_b
            law.boundary_b_lng = lng_b
        law.save()

    def fetch_geocode(self, highway, cross_street):
        """Handles calling the geocoder API endpoint to fetch lat/lng data
        for the highway (road) and cross street given. Currently uses the free tier which
        is heavily throttled"""
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
        return None, None

    def parse_geocode_xml(self, tree):
        """Given an element tree with XML from geocoder API, parse latitude and longitude
        fields.
        """
        lat, lng = None, None
        for child in tree:
            if child.tag == "latt" and child.text:
                lat = float(child.text)
                lat = Decimal(lat)
            elif child.tag == "longt" and child.text:
                lng = float(child.text)
                lng = Decimal(lng)
        return lat, lng
