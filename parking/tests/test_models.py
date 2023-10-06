from django.test import TestCase

from whereToPark.models import NoParkingByLaw, RestrictedParkingByLaw, Highway


class NoParkingByLawModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        boundary_a_lat = -90.5203
        boundary_a_lng = 29.5233
        boundary_b_lat = -94.5203
        boundary_b_lng = 30.5233
        # setup objects used by all test methods
        NoParkingByLaw.objects.create(
            source_id="1",
            schedule="15",
            schedule_name="Parking for Restricted Periods",
            highway="Ashbury Avenue",
            side="North",
            between="Glenholme Avenue and Oakwood Avenue",
            cross_street_a="Glenholme Avenue",
            cross_street_b="Oakwood Avenue",
            prohibited_times_and_or_days="12 hours",
            boundary_a_lat=boundary_a_lat,
            boundary_a_lng=boundary_a_lng,
            boundary_b_lat=boundary_b_lat,
            boundary_b_lng=boundary_b_lng,
        )

    def test_source_id(self):
        law = NoParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("source_id").verbose_name
        self.assertEqual(field_label, "source id")

    def test_schedule_label(self):
        law = NoParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("schedule").verbose_name
        self.assertEqual(field_label, "schedule")

    def test_schedule_name_label(self):
        law = NoParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("schedule_name").verbose_name
        self.assertEqual(field_label, "schedule name")

    def test_highway_label(self):
        law = NoParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("highway").verbose_name
        self.assertEqual(field_label, "highway")

    def test_side_label(self):
        law = NoParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("side").verbose_name
        self.assertEqual(field_label, "side")

    def test_between_label(self):
        law = NoParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("between").verbose_name
        self.assertEqual(field_label, "between")

    def test_cross_street_a_label(self):
        law = NoParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("cross_street_a").verbose_name
        self.assertEqual(field_label, "cross street a")

    def test_cross_street_b_label(self):
        law = NoParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("cross_street_b").verbose_name
        self.assertEqual(field_label, "cross street b")

    def test_prohibited_times_and_or_days_label(self):
        law = NoParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("prohibited_times_and_or_days").verbose_name
        self.assertEqual(field_label, "prohibited times and or days")

    def test_boundary_status_a_label(self):
        law = NoParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("boundary_status_a").verbose_name
        self.assertEqual(field_label, "boundary status a")

    def test_boundary_status_b_label(self):
        law = NoParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("boundary_status_b").verbose_name
        self.assertEqual(field_label, "boundary status b")

    def test_str_method(self):
        law = NoParkingByLaw.objects.get(id=1)
        self.assertEqual(law.__str__(), "Ashbury Avenue (North) - 1")


class RestrictedParkingByLawModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        boundary_a_lat = -90.5203
        boundary_a_lng = 29.5233
        boundary_b_lat = -94.5203
        boundary_b_lng = 30.5233
        # setup objects used by all test methods
        RestrictedParkingByLaw.objects.create(
            source_id="1",
            schedule="15",
            schedule_name="Parking for Restricted Periods",
            highway="Ashbury Avenue",
            side="North",
            between="Glenholme Avenue and Oakwood Avenue",
            cross_street_a="Glenholme Avenue",
            cross_street_b="Oakwood Avenue",
            times_and_or_days="10:00 a.m. to 6:00 p.m., Mon. to Fri.",
            max_period_permitted="12 hours",
            boundary_a_lat=boundary_a_lat,
            boundary_a_lng=boundary_a_lng,
            boundary_b_lat=boundary_b_lat,
            boundary_b_lng=boundary_b_lng,
        )

    def test_source_id(self):
        law = RestrictedParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("source_id").verbose_name
        self.assertEqual(field_label, "source id")

    def test_schedule_label(self):
        law = RestrictedParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("schedule").verbose_name
        self.assertEqual(field_label, "schedule")

    def test_schedule_name_label(self):
        law = RestrictedParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("schedule_name").verbose_name
        self.assertEqual(field_label, "schedule name")

    def test_highway_label(self):
        law = RestrictedParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("highway").verbose_name
        self.assertEqual(field_label, "highway")

    def test_side_label(self):
        law = RestrictedParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("side").verbose_name
        self.assertEqual(field_label, "side")

    def test_between_label(self):
        law = RestrictedParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("between").verbose_name
        self.assertEqual(field_label, "between")

    def test_cross_street_a_label(self):
        law = RestrictedParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("cross_street_a").verbose_name
        self.assertEqual(field_label, "cross street a")

    def test_cross_street_b_label(self):
        law = RestrictedParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("cross_street_b").verbose_name
        self.assertEqual(field_label, "cross street b")

    def test_times_and_or_day_label(self):
        law = RestrictedParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("times_and_or_days").verbose_name
        self.assertEqual(field_label, "times and or days")

    def test_max_period_permitted_label(self):
        law = RestrictedParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("max_period_permitted").verbose_name
        self.assertEqual(field_label, "max period permitted")

    def test_boundary_status_a_label(self):
        law = RestrictedParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("boundary_status_a").verbose_name
        self.assertEqual(field_label, "boundary status a")

    def test_boundary_status_b_label(self):
        law = RestrictedParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("boundary_status_b").verbose_name
        self.assertEqual(field_label, "boundary status b")

    def test_str_method(self):
        law = RestrictedParkingByLaw.objects.get(id=1)
        self.assertEqual(law.__str__(), "Ashbury Avenue (North) - 1")


class HighwayModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # setup objects used by all test methods
        Highway.objects.create(name="king street", street_end="W")

    def test_name_label(self):
        highway = Highway.objects.get(id=1)
        field_label = highway._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_street_end_label(self):
        highway = Highway.objects.get(id=1)
        field_label = highway._meta.get_field("street_end").verbose_name
        self.assertEqual(field_label, "street end")

    def test_str_method(self):
        highway = Highway.objects.get(id=1)
        self.assertEqual(highway.__str__(), "king street W")
