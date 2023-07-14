from django.core.management.base import BaseCommand, CommandError
import xml.etree.ElementTree as ET


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    # def add_arguments(self, parser):
    #     parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        parse_no_parking_bylaws()
        parse_restricted_parking_bylaws()


def parse_no_parking_bylaws():
    tree = ET.parse("./whereToPark/no_parking.xml")
    root = tree.getroot()
    for child in root:
        for attribute in child:
            print(f"{attribute.tag}: {attribute.text}")


def parse_restricted_parking_bylaws():
    tree = ET.parse("./whereToPark/restricted_parking.xml")
    root = tree.getroot()
