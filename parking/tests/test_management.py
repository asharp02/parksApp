import os
import xml.etree.ElementTree as ET

from django.core.management import call_command
from django.test import TestCase, SimpleTestCase
from whereToPark.management.commands.get_parking_dump import (
    Command as GetParkingDumpCmd,
)
from whereToPark.management.commands.import_parking_data import (
    Command as ImportParkingCmd,
)
from whereToPark.management.commands.set_location_data import Command as SetParkingCmd

from whereToPark.models import NoParkingByLaw, RestrictedParkingByLaw, Highway

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
        NoParkingByLaw.objects.create(
            source_id="1",
            schedule="15",
            schedule_name="Parking for Restricted Periods",
            highway=self.highway,
            side="North",
            between="Glenholme Avenue and Oakwood Avenue",
            prohibited_times_and_or_days="12 hours",
        )
        RestrictedParkingByLaw.objects.create(
            source_id="1",
            schedule="15",
            schedule_name="Parking for Restricted Periods",
            highway=self.highway,
            side="North",
            between="Glenholme Avenue and Oakwood Avenue",
            times_and_or_days="12 hours",
            max_period_permitted="12 hours",
        )
        call_command("set_location_data")

    def test_simple_between_field_produces_correct_lat_lng(self):
        law = NoParkingByLaw.objects.get(id=1)
        self.assertAlmostEqual(law.boundary_start.lat, 43.689936, delta=0.00005)
        self.assertAlmostEqual(law.boundary_start.lng, -79.442908, delta=0.0005)
        self.assertAlmostEqual(law.boundary_end.lat, 43.690593, delta=0.00005)
        self.assertAlmostEqual(law.boundary_end.lng, -79.440109, delta=0.0005)

    def test_simple_between_field_produces_correct_lat_lng_restricted(self):
        law = RestrictedParkingByLaw.objects.get(id=1)
        self.assertAlmostEqual(law.boundary_start.lat, 43.689936, delta=0.00005)
        self.assertAlmostEqual(law.boundary_start.lng, -79.442908, delta=0.0005)
        self.assertAlmostEqual(law.boundary_end.lat, 43.690593, delta=0.00005)
        self.assertAlmostEqual(law.boundary_end.lng, -79.440109, delta=0.0005)

    def test_complex_between_field_doesnt_save_location(self):
        NoParkingByLaw.objects.create(
            source_id="2",
            schedule="15",
            schedule_name="Parking for Restricted Periods",
            highway=self.highway,
            side="North",
            between="Brock Avenue and the west end of Abbs Street",
            prohibited_times_and_or_days="12 hours",
        )
        call_command("set_location_data")
        law = NoParkingByLaw.objects.get(id=2)
        self.assertIsNone(law.boundary_start)
        self.assertIsNone(law.boundary_end)

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

    # def test_cross_street_a_and_b_fields_set_no_parking(self):
    #     law = NoParkingByLaw.objects.first()
    #     between = law.between
    #     print(between)
    #     self.assertEqual(law.cross_street_a, between.split(" and ")[0])
    #     self.assertEqual(law.cross_street_b, between.split(" and ")[1])

    # def test_cross_street_a_and_b_fields_set_restricted(self):
    #     law = RestrictedParkingByLaw.objects.first()
    #     between = law.between
    #     self.assertEqual(law.cross_street_a, between.split(" and ")[0])
    #     self.assertEqual(law.cross_street_b, between.split(" and ")[1])

    def test_noparkingbylaw_model_count_matches_xml_file(self):
        self.assertEqual(
            NoParkingByLaw.objects.count(), len(self.np_root.getchildren())
        )

    def test_restrictedparkingbylaw_model_count_matches_xml_file(self):
        self.assertEqual(
            RestrictedParkingByLaw.objects.count(), len(self.rp_root.getchildren())
        )

    def test_no_parking_cmd_does_not_create_duplicates(self):
        total_count_pre = NoParkingByLaw.objects.count()
        call_command("import_parking_data")

        self.assertEqual(total_count_pre, NoParkingByLaw.objects.count())

        first_id = NoParkingByLaw.objects.first().source_id
        count_with_id = NoParkingByLaw.objects.filter(source_id=first_id).count()
        self.assertEqual(count_with_id, 1)

    def test_restricted_parking_cmd_does_not_create_duplicates(self):
        total_count_pre = RestrictedParkingByLaw.objects.count()
        call_command("import_parking_data")
        self.assertEqual(total_count_pre, RestrictedParkingByLaw.objects.count())

        first_id = RestrictedParkingByLaw.objects.first().source_id
        count_with_id = RestrictedParkingByLaw.objects.filter(
            source_id=first_id
        ).count()
        self.assertEqual(count_with_id, 1)

    def test_process_highway_parses_correctly(self):
        simple_highway = "King Street"
        parsed_res = ImportParkingCmd().process_highway_name(simple_highway)
        self.assertEqual(parsed_res[0], "king street")
        self.assertIsNone(parsed_res[1])

        # highway_with_end = "King Street West"
        # result = ImportParkingCmd().process_highway_name(highway_with_end)
        # self.assertEqual(result[0], "king street")
        # self.assertEqual(result[1], "west")

        # highway_with_parens = "Isaac Devins Boulevard (south branch)"
        # result = ImportParkingCmd().process_highway_name(highway_with_end)
        # self.assertEqual(result[0], "king street")
        # self.assertEqual(result[1], "west")
