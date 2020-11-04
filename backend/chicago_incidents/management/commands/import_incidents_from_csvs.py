import time
import pandas as pd
import numpy as np
import datetime

from django.core.management.base import BaseCommand, CommandParser
from chicago_incidents import models
from django.utils import timezone

datetime.datetime.now(tz=timezone.utc)


class Command(BaseCommand):
    """Command to import all types of CSVs to the database
    """
    help = 'Import all types of CSVs to the database'

    def add_arguments(self, parser: CommandParser):
        """Add the command arguments.

        :param parser: The argument parser.
        """
        parser.add_argument('input_files', nargs='+', help='The input files to parse')

    def handle(self, *args, **options):

        """Implement the logic of the command.
        """
        start = time.time()
        for input_file in options['input_files']:
            self.stdout.write(f"Processing file {input_file}")
            if input_file.endswith('abandoned-vehicles.csv'):
                self.import_abandoned_vehicles(input_file)
            else:
                self.stdout.write(f"File cannot be processed, skipping.")

        end = time.time()
        self.stdout.write(f"Finished importing abandoned vehicles, took {(end - start):.2f} seconds")

    def import_abandoned_vehicles(self, input_file: str):
        """Import the requests for abandoned vehicles to the database.

        :param input_file: The file from which to load the requests for abandoned vehicles.
        """
        self.stdout.write("Getting requests for abandoned vehicles")

        input_df = pd.read_csv(input_file, sep=',').replace({np.nan: None})
        input_df.columns = ['creation_date', 'status', 'completion_date', 'service_request_number',
                            'type_of_service_request', 'license_plate', 'vehicle_make_model', 'vehicle_color',
                            'current_activity', 'most_recent_action', 'days_of_report_as_parked', 'street_address',
                            'zip_code', 'x_coordinate', 'y_coordinate', 'ward', 'police_district', 'community_area',
                            'ssa', 'latitude', 'longitude', 'location', 'historical_wards_03_15', 'zip_codes',
                            'community_areas', 'census_tracts', 'wards']

        for row in input_df.itertuples(index=False):
            # Why we need try/except blocks:
            # We should to check that the data does not exist already in the database in  case we  imported the same
            # data multiple times
            print(row)
            # Retrieve or create the car that is involved to the current incident
            try:
                vehicle = models.Vehicle.objects.get(license_plate=row.license_plate,
                                                     vehicle_color=row.vehicle_color,
                                                     vehicle_make_model=row.vehicle_make_model)
            except models.Vehicle.DoesNotExist:
                # Do not create vehicles with None values
                if row.license_plate and row.vehicle_color and row.vehicle_make_model:
                    vehicle = models.Vehicle(license_plate=row.license_plate,
                                             vehicle_color=row.vehicle_color,
                                             vehicle_make_model=row.vehicle_make_model)
                    vehicle.save()
                else:
                    vehicle = None

            # TODO this could be a separate method because all incidents we import will have this chunk of code
            # Retrieve or create the current incident
            try:
                incident = models.Incident.objects.get(creation_date=row.creation_date,
                                                       status=self.get_status_type(row.status),
                                                       completion_date=row.completion_date,
                                                       service_request_number=row.service_request_number,
                                                       type_of_service_request=self.get_request_type(
                                                           row.type_of_service_request),
                                                       current_activity=row.current_activity,
                                                       most_recent_action=row.most_recent_action,
                                                       street_address=row.street_address, zip_code=row.zip_code)
            except models.Incident.DoesNotExist:
                incident = models.Incident(creation_date=row.creation_date,
                                           status=self.get_status_type(row.status),
                                           completion_date=row.completion_date,
                                           service_request_number=row.service_request_number,
                                           type_of_service_request=self.get_request_type(row.type_of_service_request),
                                           current_activity=row.current_activity,
                                           most_recent_action=row.most_recent_action,
                                           street_address=row.street_address, zip_code=row.zip_code,
                                           zip_codes=row.zip_codes, x_coordinate=row.x_coordinate,
                                           y_coordinate=row.y_coordinate, ward=row.ward, wards=row.wards,
                                           historical_wards_03_15=row.historical_wards_03_15,
                                           police_district=row.police_district,
                                           community_area=row.community_area,
                                           community_areas=row.community_areas, ssa=row.ssa,
                                           census_tracts=row.census_tracts, latitude=row.latitude,
                                           longitude=row.longitude, location=row.location)
                incident.save()

            if vehicle:
                try:
                    _ = models.AbandonedVehicle.objects.get(vehicle=vehicle, incident=incident,
                                                            days_of_report_as_parked=row.days_of_report_as_parked)
                except models.AbandonedVehicle.DoesNotExist:
                    abandoned_vehicle = models.AbandonedVehicle(vehicle=vehicle, incident=incident,
                                                                days_of_report_as_parked=row.days_of_report_as_parked)
                    abandoned_vehicle.save()

    @staticmethod
    def get_status_type(value: str) -> str:
        for x in models.Incident.STATUS_TYPE_CHOICES:
            if x[1] == value:
                return x[0]

    @staticmethod
    def get_request_type(value: str) -> str:
        for x in models.Incident.SERVICE_TYPE_CHOICES:
            if x[1] == value:
                return x[0]
