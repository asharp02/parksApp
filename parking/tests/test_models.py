from django.test import TestCase

from whereToPark.models import NoParkingByLaw, RestrictedParkingByLaw


class NoParkingByLawModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # setup objects used by all test methods
        NoParkingByLaw.objects.create(
            bylaw_no="[Repealed 2016-04-05 by By-law No. 365-2016]",
            source_id="1",
            schedule="15",
            schedule_name="Parking for Restricted Periods",
            highway="Ashbury Avenue",
            side="North",
            between="Glenholme Avenue and Oakwood Avenue",
            times_and_or_days="10:00 a.m. to 6:00 p.m., Mon. to Fri.",
            prohibited_times_and_or_days="12 hours",
        )

    def test_bylaw_no_label(self):
        law = NoParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("bylaw_no").verbose_name
        self.assertEqual(field_label, "bylaw no")

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

    def test_times_and_or_day_label(self):
        law = NoParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("times_and_or_days").verbose_name
        self.assertEqual(field_label, "times and or days")

    def test_max_period_permitted_label(self):
        law = NoParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("prohibited_times_and_or_days").verbose_name
        self.assertEqual(field_label, "prohibited times and or days")


class RestrictedParkingByLawModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # setup objects used by all test methods
        RestrictedParkingByLaw.objects.create(
            bylaw_no="[Repealed 2016-04-05 by By-law No. 365-2016]",
            source_id="1",
            schedule="15",
            schedule_name="Parking for Restricted Periods",
            highway="Ashbury Avenue",
            side="North",
            between="Glenholme Avenue and Oakwood Avenue",
            times_and_or_days="10:00 a.m. to 6:00 p.m., Mon. to Fri.",
            max_period_permitted="12 hours",
        )

    def test_bylaw_no_label(self):
        law = RestrictedParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("bylaw_no").verbose_name
        self.assertEqual(field_label, "bylaw no")

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

    def test_times_and_or_day_label(self):
        law = RestrictedParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("times_and_or_days").verbose_name
        self.assertEqual(field_label, "times and or days")

    def test_max_period_permitted_label(self):
        law = RestrictedParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("max_period_permitted").verbose_name
        self.assertEqual(field_label, "max period permitted")
