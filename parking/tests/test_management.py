import os
import xml.etree.ElementTree as ET

from django.core.management import call_command
from django.test import TestCase, SimpleTestCase
from unittest import skip
from whereToPark.management.commands.get_parking_dump import (
    Command as GetParkingDumpCmd,
)
from whereToPark.management.commands.import_parking_data import (
    Command as ImportParkingCmd,
)
from whereToPark.management.commands.set_location_data import Command as SetParkingCmd

from whereToPark.models import ByLaw, Highway, Intersection

# Create your tests here.


def file_exists(directory, filename):
    root_path = os.getcwd()
    file_path = os.path.join(root_path, directory, filename)
    return os.path.exists(file_path)


class GetParkingDumpTests(SimpleTestCase):
    def test_fetch_data_folder_outputs_zipped_folder(self):
        GetParkingDumpCmd().fetch_data_folder()
        directory = ""
        filename = "parking_schedules.zip"
        self.assertTrue(file_exists(directory, filename))

    def test_unzip_files_in_right_folder(self):
        GetParkingDumpCmd().unzip_files()
        directory = "fixtures"
        no_parking_filename = "no_parking.xml"
        restricted_parking_filename = "restricted_parking.xml"
        self.assertTrue(file_exists(directory, no_parking_filename))
        self.assertTrue(file_exists(directory, restricted_parking_filename))


class SetLocationDataTests(TestCase):
    def setUp(self):
        self.highway = Highway.objects.create(name="ashbury avenue")
        self.highway.save()
        self.cross_highway_a = Highway.objects.create(name="glenholme avenue")
        self.cross_highway_a.save()
        self.cross_highway_b = Highway.objects.create(name="oakwood avenue")
        self.cross_highway_b.save()

        ByLaw.objects.create(
            source_id="1",
            schedule="13",
            schedule_name="Parking for Restricted Periods",
            highway=self.highway,
            side="North",
            between="glenholme avenue and oakwood avenue",
            times_and_or_days="12 hours",
        )
        call_command("set_location_data")

    def test_intersection_a_imported(self):
        intersections = Intersection.objects.filter(
            main_street=self.highway, cross_street=self.cross_highway_a
        )
        self.assertEqual(intersections.count(), 1)
        intersection = intersections.first()
        self.assertEqual(intersection.main_street, self.highway)
        self.assertEqual(intersection.cross_street, self.cross_highway_a)

    def test_intersection_b_imported(self):
        intersections = Intersection.objects.filter(
            main_street=self.highway, cross_street=self.cross_highway_b
        )
        self.assertEqual(intersections.count(), 1)
        intersection = intersections.first()
        self.assertEqual(intersection.main_street, self.highway)
        self.assertEqual(intersection.cross_street, self.cross_highway_b)

    def test_bylaw_boundary_start_set_correctly(self):
        bylaw = ByLaw.objects.first()
        intersection = Intersection.objects.filter(
            main_street=self.highway, cross_street=self.cross_highway_a
        ).first()
        self.assertEqual(bylaw.boundary_start, intersection)

    def test_bylaw_boundary_end_set_correctly(self):
        bylaw = ByLaw.objects.first()
        intersection = Intersection.objects.filter(
            main_street=self.highway, cross_street=self.cross_highway_b
        ).first()
        self.assertEqual(bylaw.boundary_end, intersection)

    @skip("Refactoring")
    def test_simple_between_field_produces_correct_lat_lng(self):
        law = ByLaw.objects.get(id=1)
        self.assertAlmostEqual(law.boundary_start.lat, 43.689936, delta=0.00005)
        self.assertAlmostEqual(law.boundary_start.lng, -79.442908, delta=0.0005)
        self.assertAlmostEqual(law.boundary_end.lat, 43.690593, delta=0.00005)
        self.assertAlmostEqual(law.boundary_end.lng, -79.440109, delta=0.0005)

    @skip("Refactoring")
    def test_simple_between_field_produces_correct_lat_lng_restricted(self):
        law = ByLaw.objects.get(id=1)
        self.assertAlmostEqual(law.boundary_start.lat, 43.689936, delta=0.00005)
        self.assertAlmostEqual(law.boundary_start.lng, -79.442908, delta=0.0005)
        self.assertAlmostEqual(law.boundary_end.lat, 43.690593, delta=0.00005)
        self.assertAlmostEqual(law.boundary_end.lng, -79.440109, delta=0.0005)

    @skip("Refactoring")
    def test_complex_between_field_doesnt_save_location(self):
        ByLaw.objects.create(
            source_id="2",
            schedule="15",
            schedule_name="Parking for Restricted Periods",
            highway=self.highway,
            side="North",
            between="Brock Avenue and the west end of Abbs Street",
            prohibited_times_and_or_days="12 hours",
        )
        call_command("set_location_data")
        law = ByLaw.objects.get(id=2)
        self.assertIsNone(law.boundary_start)
        self.assertIsNone(law.boundary_end)

    @skip("Refactoring")
    def test_parse_geocode_xml(self):
        sample_xml = "<geodata>\
                        <latt>43.690601</latt>\
                        <longt>-79.439944</longt>\
                        <city>toronto</city>\
                        <prov>ON</prov>\
                        <street1>ashbury avenue</street1>\
                        <street2>oakwood avenue</street2>\
                        <confidence>0.9</confidence>\
                    </geodata>"
        tree = ET.fromstring(sample_xml)
        (lat, lng), _ = SetParkingCmd().parse_geocode_xml(tree)
        self.assertEqual(lat, 43.690601)
        self.assertEqual(lng, -79.439944)


class ImportParkingDataTests(TestCase):
    def setUp(self):
        call_command("import_parking_data")
        np_tree = ET.parse("fixtures/no_parking.xml")
        self.np_root = np_tree.getroot()

        rp_tree = ET.parse("fixtures/restricted_parking.xml")
        self.rp_root = rp_tree.getroot()

    def test_noparkingbylaw_model_count_matches_xml_file(self):
        self.assertEqual(
            ByLaw.objects.filter(schedule="13").count(), len(self.np_root.getchildren())
        )

    def test_restrictedparkingbylaw_model_count_matches_xml_file(self):
        self.assertEqual(
            ByLaw.objects.filter(schedule="15").count(), len(self.rp_root.getchildren())
        )

    def test_no_parking_cmd_does_not_create_duplicates(self):
        total_count_pre = ByLaw.objects.count()
        call_command("import_parking_data")

        self.assertEqual(total_count_pre, ByLaw.objects.count())

    def test_process_highway_parses_correctly(self):
        simple_highway = {"highway": "king street"}
        parsed_res = ImportParkingCmd().process_highway_name(simple_highway)
        self.assertEqual(simple_highway["highway"], "king street")

    def test_process_highway_parses_correctly_with_parens(self):
        highway_with_parens = {"highway": "isaac devins boulevard (south branch)"}
        result = ImportParkingCmd().process_highway_name(highway_with_parens)
        self.assertEqual(highway_with_parens["highway"], "isaac devins boulevard")
