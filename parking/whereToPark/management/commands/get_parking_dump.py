from django.core.management.base import BaseCommand, CommandError
import requests
from zipfile import ZipFile


class Command(BaseCommand):
    """
    This management command fetches the Traffic and parking by-law schedules ZIP folder
    on the Toronto Open Data CKAN instance. The command unzips the folder and stores two
    files that we need locally ("Ch_950_Sch_13_NoParking_current_to_MMDDYYYY" and
    "Ch_950_Sch_15_ParkingForRestrictedPeriods_current_to_MMDDYYYY"). API documentation
    can be accessed here: https://docs.ckan.org/en/latest/api/
    """

    help = "Reaches out to Toronto Open Data API, fetches parking data and stores the files locally."

    # def add_arguments(self, parser):
    #     parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        self.fetch_data_folder()
        self.unzip_files()

    def fetch_data_folder(self):
        """Makes a GET request to API, if succesful, creates a parking_schedules folder with contents
        of response (ZIP)"""
        base_url = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
        url = base_url + "/api/3/action/package_show"
        params = {"id": "traffic-and-parking-by-law-schedules"}
        package = requests.get(url, params=params).json()
        for idx, resource in enumerate(package["result"]["resources"]):
            if resource["name"] != "Traffic and parking by-law schedules":
                continue
            # To get metadata for non datastore_active resources:
            url = base_url + "/api/3/action/resource_show?id=" + resource["id"]
            resource_metadata = requests.get(url).json()
            if resource_metadata["success"] != True:
                print(
                    "Error: dataset fetch was unsuccesful"
                )  # TODO Replace with logger
                return
            response = requests.get(resource["url"])
            if response.status_code != 200:
                print(
                    "Error: dataset fetch was unsuccesful"
                )  # TODO Replace with logger
                return
            with open("parking_schedules.zip", mode="wb") as file:
                file.write(response.content)

    def unzip_files(self):
        """Unzips the necessary files within the zipped parking_schedules folder"""
        with ZipFile("parking_schedules.zip", "r") as zObject:
            no_parking_filename = "Ch_950_Sch_13_NoParking_current_to_Feb242021.xml"
            restricted_parking_filename = (
                "Ch_950_Sch_15_ParkingForRestrictedPeriods_current_to_Feb242021.xml"
            )
            zObject.extract(no_parking_filename, path="fixtures")
            zObject.extract(restricted_parking_filename, path="fixtures")
