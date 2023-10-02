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

    def test_noparkingbylaw_model_count_matches_xml_file(self):
        tree = ET.parse("fixtures/no_parking.xml")
        root = tree.getroot()

        self.assertEqual(NoParkingByLaw.objects.count(), len(root.getchildren()))

    def test_restrictedparkingbylaw_model_count_matches_xml_file(self):
        tree = ET.parse("fixtures/restricted_parking.xml")
        root = tree.getroot()
        self.assertEqual(
            RestrictedParkingByLaw.objects.count(), len(root.getchildren())
        )
