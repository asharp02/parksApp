import xml.etree.ElementTree as ET

from django.core.management.base import BaseCommand, CommandError

from whereToPark.models import NoParkingByLaw, RestrictedParkingByLaw

FIELD_MAPPINGS = {
    "ByLawNo": "bylaw_no",
    "ID": "source_id",
    "Schedule": "schedule",
    "ScheduleName": "schedule_name",
    "Highway": "highway",
    "Side": "side",
    "Between": "between",
    "Prohibited_Times_and_or_Days": "prohibited_times_and_or_days",
    "Maximum_Period_Permitted": "max_period_permitted",
    "Times_and_or_Days": "times_and_or_days",
}


class Command(BaseCommand):
    """This mgmt command imports the data found within the 'fixtures' folder
    into respective models either NoParkingByLaw or RestrictedParkingByLaw.
    """

    def handle(self, *args, **options):
        self.import_no_parking()
        self.import_restricted_parking()

    def import_no_parking(self):
        tree = ET.parse("fixtures/no_parking.xml")
        root = tree.getroot()
        for child in root:
            attributes = {}
            for item in child:
                if item.tag not in FIELD_MAPPINGS.keys():
                    continue
                attributes[FIELD_MAPPINGS[item.tag]] = item.text
                attributes["source_id"] = int(attributes["source_id"])
            law, _ = NoParkingByLaw.objects.update_or_create(
                source_id=attributes["source_id"], defaults=attributes
            )
            law.save()

    def import_restricted_parking(self):
        tree = ET.parse("fixtures/restricted_parking.xml")
        root = tree.getroot()
        for child in root:
            attributes = {}
            for item in child:
                if item.tag not in FIELD_MAPPINGS.keys():
                    continue
                attributes[FIELD_MAPPINGS[item.tag]] = item.text
                attributes["source_id"] = int(attributes["source_id"])
            law, _ = RestrictedParkingByLaw.objects.update_or_create(
                source_id=attributes["source_id"], defaults=attributes
            )
            law.save()
