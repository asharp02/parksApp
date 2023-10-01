import os
import xml.etree.ElementTree as ET

from django.test import TestCase, SimpleTestCase
from whereToPark.management.commands.get_parking_dump import Command
from whereToPark.models import NoParkingByLaw, RestrictedParkingByLaw

# Create your tests here.


def file_exists(directory, filename):
    root_path = os.getcwd()
    file_path = os.path.join(root_path, directory, filename)
    return os.path.exists(file_path)


class GetParkingDumpTests(SimpleTestCase):
    def test_fetch_data_folder_outputs_zipped_folder(self):
        Command().fetch_data_folder()
        directory = ""
        filename = "parking_schedules.zip"
        self.assertTrue(file_exists(directory, filename))

    def test_unzip_files_in_right_folder(self):
        Command().unzip_files()
        directory = "fixtures"
        no_parking_filename = "no_parking.xml"
        restricted_parking_filename = "restricted_parking.xml"
        self.assertTrue(file_exists(directory, no_parking_filename))
        self.assertTrue(file_exists(directory, restricted_parking_filename))


class ImportParkingDataTests(TestCase):
    def test_model_count_matches_xml_files(self):
        pass
        # no_parking_tree = ET.parse("fixtures/no_parking.xml")
        # no_parking_root = no_parking_tree.getroot()

        # restricted_parking_tree = ET.parse("fixtures/restricted_parking.xml")
        # print(len(no_parking_root.getchildren()))
        # ParkingByLaw.objects.count()
        # self.assertEqual(ParkingByLaw.objects.count())

        # restricted_tree = ET.parse("fixtures/restricted_parking.xml")
