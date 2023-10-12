import xml.etree.ElementTree as ET

from django.core.management.base import BaseCommand, CommandError

from whereToPark.models import (
    NoParkingByLaw,
    RestrictedParkingByLaw,
    Highway,
    Intersection,
)

FIELD_MAPPINGS = {
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
    restricted_bylaws = []
    intersections = []
    intersections_created = []

    def handle(self, *args, **options):
        self.no_parking_bylaws = self.fetch_bylaws(False)
        self.restricted_bylaws = self.fetch_bylaws(True)
        self.import_highways()
        # self.import_bylaws()
        self.import_intersections()

    def import_intersections(self):
        objs = []
        for bylaw in self.no_parking_bylaws + self.restricted_bylaws:
            intersections = self.parse_between_field(bylaw)
            for main, cross in intersections:
                print(main, cross)
                if not main or not cross:
                    continue
                highway_main = Highway.objects.filter(name=main).first()
                highway_cross = Highway.objects.filter(name=cross).first()
                objs.append(
                    Intersection(main_street=highway_main, cross_street=highway_cross)
                )

        self.intersections_created = Intersection.objects.bulk_create(
            objs, ignore_conflicts=True
        )

    def import_highways(self):
        highway_names = map(
            lambda x: self.process_highway_name(x["highway"]),
            self.no_parking_bylaws + self.restricted_bylaws,
        )

        highway_objs = []
        for parsed_name, end in set(highway_names):
            if parsed_name:
                obj = Highway(name=parsed_name.lower())
                highway_objs.append(obj)

        Highway.objects.bulk_create(highway_objs, ignore_conflicts=True)

    def process_highway_name(self, name):
        """Given a highway name from the XML source, returns a tuple containing
        the parsed name and the direction/end of the street. Removes parens
        from name for cases like 'College Street (North Branch)'.
        """
        # Remove content contained in parens if present
        tokens = name.split("(")
        if len(tokens) >= 2:
            name = "".join(tokens[:-1]).strip()

        tokens = name.split(" ")
        if len(tokens) <= 1:
            return (None, None)

        return (name.lower(), None)
        # last_word = tokens[-1]
        # if last_word.lower() in ["west", "south", "east", "north"]:
        #     return (" ".join(tokens[:-1]).lower(), last_word.lower())
        # return (name.lower(), None)

    def import_bylaws(self):
        np_entries = map(lambda x: NoParkingByLaw(**x), self.no_parking_bylaws)
        restricted_entries = map(
            lambda x: RestrictedParkingByLaw(**x), self.restricted_bylaws
        )

        intersections_by_pk = self.fetch_intersection_objs()

        NoParkingByLaw.objects.bulk_create(np_entries, ignore_conflicts=True)
        RestrictedParkingByLaw.objects.bulk_create(
            restricted_entries, ignore_conflicts=True
        )

    def fetch_intersection_objs(self):
        res = {}
        for intersection in self.intersections_created:
            pass

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
                if item.tag == "ByLawNo":  # Bylaw has been repealed, we can skip
                    break
                if not item.text:
                    continue
                attributes[FIELD_MAPPINGS[item.tag]] = item.text.lower()
                attributes["source_id"] = int(attributes["source_id"])
            self.handle_between_field(attributes)
            records.append(attributes)
        return records

    def parse_between_field(self, attributes):
        res = []
        if "between" not in attributes or attributes["between"] == None:
            return res
        cross_streets = attributes["between"].split(" and ")
        print(cross_streets)
        if len(cross_streets) != 2:
            return res
        cross_street_a = cross_streets[0].lower()
        cross_street_b = cross_streets[1].lower()
        found_a = Highway.objects.filter(name=cross_street_a).count() > 0
        found_b = Highway.objects.filter(name=cross_street_b).count() > 0
        if found_a and found_b:
            res.append((attributes["highway"], cross_street_a))
            res.append((attributes["highway"], cross_street_b))
        return res
