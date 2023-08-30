from django.core.management.base import BaseCommand, CommandError
import requests


class Command(BaseCommand):
    help = "Reaches out to Toronto Open Data API, fetches parking data and stores the files locally."

    # def add_arguments(self, parser):
    #     parser.add_argument("poll_ids", nargs="+", type=int)

    """
        This management command fetches the Traffic and parking by-law schedules ZIP folder
        on the Toronto Open Data CKAN instance. The command unzips the folder and stores two
        files that we need locally ("Ch_950_Sch_13_NoParking_current_to_MMDDYYYY" and 
        "Ch_950_Sch_15_ParkingForRestrictedPeriods_current_to_MMDDYYYY"). API documentation
        can be accessed here: https://docs.ckan.org/en/latest/api/
    """
    def handle(self, *args, **options):

        fetch_data_folder()
    

def fetch_data_folder():
    base_url = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
    url = base_url + "/api/3/action/package_show"
    params = { "id": "traffic-and-parking-by-law-schedules"}
    package = requests.get(url, params = params).json()
    for idx, resource in enumerate(package["result"]["resources"]):
        print(resource)
        # To get metadata for non datastore_active resources:
        if not resource["datastore_active"]:
            url = base_url + "/api/3/action/resource_show?id=" + resource["id"]
            resource_metadata = requests.get(url).json()
            print(resource_metadata)