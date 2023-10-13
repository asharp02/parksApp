import xml.etree.ElementTree as ET

from django.core.management.base import BaseCommand, CommandError

from whereToPark.models import (
    ByLaw,
    Highway,
    ByLaw,
)

FIELD_MAPPINGS = {
    "ID": "source_id",
    "Schedule": "schedule",
    "ScheduleName": "schedule_name",
    "Highway": "highway",
    "Side": "side",
    "Between": "between",
    "Prohibited_Times_and_or_Days": "times_and_or_days",
    "Maximum_Period_Permitted": "max_period_permitted",
    "Times_and_or_Days": "times_and_or_days",
}


class Command(BaseCommand):
    """This mgmt command imports the data found within the 'fixtures' folder
    into respective models either NoParkingByLaw or RestrictedParkingByLaw.
    """

    def handle(self, *args, **options):
        self.bylaws = self.fetch_bylaws("fixtures/restricted_parking.xml")
        self.bylaws.extend(self.fetch_bylaws("fixtures/no_parking.xml"))
        self.import_highways()
        self.import_bylaws()

    def import_highways(self):
        highway_objs = [Highway(name=bylaw["highway"]) for bylaw in self.bylaws]

        Highway.objects.bulk_create(highway_objs, ignore_conflicts=True)

        for entry in self.bylaws:
            highway_name = entry["highway"]
            entry["highway"] = Highway.objects.filter(name=highway_name).first()

    def process_highway_name(self, attributes):
        """Given a highway name from the XML source, returns a tuple containing
        the parsed name and the direction/end of the street. Removes parens
        from name for cases like 'College Street (North Branch)'.
        """
        # Remove content contained in parens if present
        tokens = attributes["highway"].split("(")
        if len(tokens) >= 2:
            attributes["highway"] = "".join(tokens[:-1]).strip()

    def import_bylaws(self):
        entries = map(lambda x: ByLaw(**x), self.bylaws)

        ByLaw.objects.bulk_create(
            entries,
            update_conflicts=True,
            update_fields=["highway"],
            unique_fields=["schedule", "source_id"],
        )

    def fetch_bylaws(self, xml_file):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        records = []
        for child in root:
            attributes = {}
            for item in child:
                if item.tag not in FIELD_MAPPINGS.keys():
                    continue
                if item.tag == "ByLawNo":  # Bylaw has been repealed, we can skip
                    break
                if not item.text:
                    break
                attributes[FIELD_MAPPINGS[item.tag]] = item.text.lower()
                attributes["source_id"] = int(attributes["source_id"])
            self.process_highway_name(attributes)
            records.append(attributes)
        return records
