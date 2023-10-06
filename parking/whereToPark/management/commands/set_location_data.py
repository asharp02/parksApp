from urllib3.util import Retry
from requests import Session
import time
from requests.exceptions import RetryError
from requests.adapters import HTTPAdapter
from xml.etree import ElementTree as ET
from decimal import Decimal

from django.db.models import Q
from django.core.management.base import BaseCommand, CommandError

from whereToPark.models import NoParkingByLaw, RestrictedParkingByLaw

GEOCODER_API_ENDPOINT = "https://geocoder.ca/"
URL_PARAMS = "&city=toronto&geoit=xml"


class Command(BaseCommand):
    # represents list of np/rp bylaw objs with updated boundaries
    np_with_locations = []
    rp_with_locations = []
    timeout_count = 0

    def handle(self, *args, **options):
        self.np_with_locations = self.fetch_bylaws_with_loc(False)
        self.rp_with_locations = self.fetch_bylaws_with_loc(True)
        update_fields = [
            "boundary_a_lat",
            "boundary_a_lng",
            "boundary_b_lat",
            "boundary_b_lng",
            "boundary_status_a",
            "boundary_status_b",
        ]
        NoParkingByLaw.objects.bulk_update(self.np_with_locations, update_fields)
        RestrictedParkingByLaw.objects.bulk_update(
            self.rp_with_locations, update_fields
        )
        (self.np_with_locations)
        print(self.rp_with_locations)

    def fetch_bylaws_with_loc(self, restricted):
        laws = []
        model = RestrictedParkingByLaw if restricted else NoParkingByLaw
        exclude_q = (
            Q(bylaw_no__icontains="repealed")
            | Q(cross_street_a=None)
            | Q(cross_street_b=None)
            | Q(boundary_status_a__in=["FS", "FNF"])
            | Q(boundary_status_b__in=["FS", "FNF"])
        )
        for bylaw in model.objects.exclude(exclude_q)[:5]:
            self.set_boundaries(bylaw)
            laws.append(bylaw)
            if self.timeout_count >= 5:
                break
        return laws

    def set_boundaries(self, law):
        (lat_a, lng_a), status_a = self.fetch_geocode(law.highway, law.cross_street_a)
        (lat_b, lng_b), status_b = self.fetch_geocode(law.highway, law.cross_street_b)
        if lat_a and lng_a and lat_b and lng_b:
            law.boundary_a_lat = lat_a
            law.boundary_a_lng = lng_a
            law.boundary_b_lat = lat_b
            law.boundary_b_lng = lng_b
        law.boundary_status_a = status_a
        law.boundary_status_b = status_b

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
