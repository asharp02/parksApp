from django.test import TestCase

from whereToPark.models import (
    ByLaw,
    Highway,
    Intersection,
)


class ByLawModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.highway = Highway.objects.create(name="queen street")
        cross_street_1 = Highway.objects.create(name="dowling avenue")
        cross_street_2 = Highway.objects.create(name="jameson avenue")

        cls.intersection_1 = Intersection.objects.create(
            main_street=cls.highway,
            cross_street=cross_street_1,
            lat=-90.5203,
            lng=29.5233,
            status="FNF",
        )
        cls.intersection_2 = Intersection.objects.create(
            main_street=cls.highway,
            cross_street=cross_street_2,
            lat=-90.5203,
            lng=29.5233,
            status="FNF",
        )

        # setup objects used by all test methods
        ByLaw.objects.create(
            source_id="1",
            schedule="15",
            schedule_name="Parking for Restricted Periods",
            highway=cls.highway,
            boundary_start=cls.intersection_1,
            boundary_end=cls.intersection_2,
            side="North",
            between="Dowling Avenue and Jameson Avenue",
            times_and_or_days="12 hours",
            max_period_permitted="12 hours",
        )

    def test_source_id(self):
        law = ByLaw.objects.get(id=1)
        field_label = law._meta.get_field("source_id").verbose_name
        self.assertEqual(field_label, "source id")

    def test_schedule_label(self):
        law = ByLaw.objects.get(id=1)
        field_label = law._meta.get_field("schedule").verbose_name
        self.assertEqual(field_label, "schedule")

    def test_schedule_name_label(self):
        law = ByLaw.objects.get(id=1)
        field_label = law._meta.get_field("schedule_name").verbose_name
        self.assertEqual(field_label, "schedule name")

    def test_highway_label(self):
        law = ByLaw.objects.get(id=1)
        field_label = law._meta.get_field("highway").verbose_name
        self.assertEqual(field_label, "highway")

    def test_side_label(self):
        law = ByLaw.objects.get(id=1)
        field_label = law._meta.get_field("side").verbose_name
        self.assertEqual(field_label, "side")

    def test_between_label(self):
        law = ByLaw.objects.get(id=1)
        field_label = law._meta.get_field("between").verbose_name
        self.assertEqual(field_label, "between")

    def test_times_and_or_days_label(self):
        law = ByLaw.objects.get(id=1)
        field_label = law._meta.get_field("times_and_or_days").verbose_name
        self.assertEqual(field_label, "times and or days")

    def test_boundary_start_label(self):
        law = ByLaw.objects.get(id=1)
        field_label = law._meta.get_field("boundary_start").verbose_name
        self.assertEqual(field_label, "boundary start")

    def test_boundary_end_label(self):
        law = ByLaw.objects.get(id=1)
        field_label = law._meta.get_field("boundary_end").verbose_name
        self.assertEqual(field_label, "boundary end")

    def test_str_method(self):
        law = ByLaw.objects.get(id=1)
        self.assertEqual(law.__str__(), "queen street (North) - 1")

    def test_max_period_permitted_label(self):
        law = ByLaw.objects.get(id=1)
        field_label = law._meta.get_field("max_period_permitted").verbose_name
        self.assertEqual(field_label, "max period permitted")


class HighwayModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # setup objects used by all test methods
        Highway.objects.create(name="king street")

    def test_name_label(self):
        highway = Highway.objects.get(id=1)
        field_label = highway._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_str_method(self):
        highway = Highway.objects.get(id=1)
        self.assertEqual(highway.__str__(), "king street")


class IntersectionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # setup objects used by all test methods
        main_street = Highway.objects.create(name="king street")
        cross_street = Highway.objects.create(name="dowling avenue")

        cls.intersection = Intersection.objects.create(
            main_street=main_street,
            cross_street=cross_street,
            lat=-90.5203,
            lng=29.5233,
            status="FNF",
        )

    def test_main_street_label(self):
        field_label = self.intersection._meta.get_field("main_street").verbose_name
        self.assertEqual(field_label, "main street")

    def test_cross_street_label(self):
        field_label = self.intersection._meta.get_field("cross_street").verbose_name
        self.assertEqual(field_label, "cross street")

    def test_lat_label(self):
        field_label = self.intersection._meta.get_field("lat").verbose_name
        self.assertEqual(field_label, "lat")

    def test_lng_label(self):
        field_label = self.intersection._meta.get_field("lng").verbose_name
        self.assertEqual(field_label, "lng")

    def test_status_label(self):
        field_label = self.intersection._meta.get_field("status").verbose_name
        self.assertEqual(field_label, "status")

    def test_str_method(self):
        main = self.intersection.main_street.name
        cross = self.intersection.cross_street.name
        status = self.intersection.status
        self.assertEqual(self.intersection.__str__(), f"{main} at {cross} ({status})")
