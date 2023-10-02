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

from whereToPark.models import NoParkingByLaw, RestrictedParkingByLaw

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


class ImportParkingDataTests(TestCase):
    def setUp(self):
        call_command("import_parking_data")
        np_tree = ET.parse("fixtures/no_parking.xml")
        self.np_root = np_tree.getroot()

        rp_tree = ET.parse("fixtures/restricted_parking.xml")
        self.rp_root = rp_tree.getroot()

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
        ImportParkingCmd().import_no_parking()

        self.assertEqual(total_count_pre, NoParkingByLaw.objects.count())

        first_id = NoParkingByLaw.objects.first().source_id
        count_with_id = NoParkingByLaw.objects.filter(source_id=first_id).count()
        self.assertEqual(count_with_id, 1)

    def test_restricted_parking_cmd_does_not_create_duplicates(self):
        total_count_pre = RestrictedParkingByLaw.objects.count()
        ImportParkingCmd().import_restricted_parking()
        self.assertEqual(total_count_pre, RestrictedParkingByLaw.objects.count())

        first_id = RestrictedParkingByLaw.objects.first().source_id
        count_with_id = RestrictedParkingByLaw.objects.filter(
            source_id=first_id
        ).count()
        self.assertEqual(count_with_id, 1)
