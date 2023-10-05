import xml.etree.ElementTree as ET

from django.core.management.base import BaseCommand, CommandError

from whereToPark.models import NoParkingByLaw, RestrictedParkingByLaw, Highway

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

    no_parking_bylaws = []
    restricted_parking_bylaws = []

    def handle(self, *args, **options):
        self.no_parking_bylaws = self.fetch_bylaws(False)
        self.restricted_bylaws = self.fetch_bylaws(True)
        self.import_highways()

    def import_highways(self):
        highway_names = map(
            lambda x: self.process_highway_name(x["highway"]),
            self.no_parking_bylaws + self.restricted_bylaws,
        )

        highway_objs = []
        for parsed_name, end in set(highway_names):
            if parsed_name:
                obj = Highway(name=parsed_name, street_end=end)
                highway_objs.append(obj)
        Highway.objects.all().delete()
        Highway.objects.bulk_create(highway_objs)

    def process_highway_name(self, name):
        # Remove content contained in parens if present
        tokens = name.split("(")
        if len(tokens) >= 2:
            name = "".join(tokens[:-1]).strip()

        tokens = name.split(" ")
        if len(tokens) <= 1:
            return (None, None)
        last_word = tokens[-1]
        if last_word.lower() in ["west", "south", "east", "north"]:
            return (" ".join(tokens[:-1]).lower(), last_word.lower())
        return (name.lower(), None)

    def fetch_bylaws(self, restricted):
        restricted_file = "fixtures/restricted_parking.xml"
        no_parking_file = "fixtures/no_parking.xml"
        xml_file = restricted_file if restricted else no_parking_file
        tree = ET.parse(xml_file)
        root = tree.getroot()
        records = []
        for child in root:
            attributes = {}
            for item in child:
                if item.tag not in FIELD_MAPPINGS.keys():
                    continue
                attributes[FIELD_MAPPINGS[item.tag]] = item.text
                attributes["source_id"] = int(attributes["source_id"])
            self.handle_between_field(attributes)
            records.append(attributes)
        return records
        # law, _ = NoParkingByLaw.objects.update_or_create(
        #     source_id=attributes["source_id"], defaults=attributes
        # )
        # law.save()

    def handle_between_field(self, attributes):
        if "between" not in attributes or attributes["between"] == None:
            return
        street_split = attributes["between"].split(" and ")
        if len(street_split) == 2:
            attributes["cross_street_a"] = street_split[0]
            attributes["cross_street_b"] = street_split[1]
