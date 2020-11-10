import time
import pandas as pd
import numpy as np
import hashlib

from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction

from chicago_incidents import models


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
            elif input_file.endswith('alley-lights-out.csv'):
                self.import_alley_lights_out_or_street_lights_all_out(input_file, street_lights=False)
            elif input_file.endswith('garbage-carts.csv'):
                self.import_garbage_carts(input_file)
            elif input_file.endswith('street-lights-all-out.csv'):
                self.import_alley_lights_out_or_street_lights_all_out(input_file, street_lights=True)
            elif input_file.endswith('street-lights-one-out.csv'):
                self.import_street_lights_one_out(input_file)
            else:
                self.stdout.write(f"File '{input_file}' cannot be processed, skipping.")

        end = time.time()
        self.stdout.write(f"Finished importing datasets, took {(end - start):.2f} seconds")

    def import_abandoned_vehicles(self, input_file: str):
        """Import the requests for abandoned abandoned_vehicles to the database.

        :param input_file: The file from which to load the requests for abandoned abandoned_vehicles.
        """
        self.stdout.write("Getting requests for abandoned vehicles")

        input_df = pd.read_csv(input_file, sep=',').replace({np.nan: None})
        input_df.columns = ['creation_date', 'status', 'completion_date', 'service_request_number',
                            'type_of_service_request', 'license_plate', 'vehicle_make_model', 'vehicle_color',
                            'current_activity', 'most_recent_action', 'days_of_report_as_parked', 'street_address',
                            'zip_code', 'x_coordinate', 'y_coordinate', 'ward', 'police_district', 'community_area',
                            'ssa', 'latitude', 'longitude', 'location', 'historical_wards_03_15', 'zip_codes',
                            'community_areas', 'census_tracts', 'wards']

        input_df = self.dataframe_normalization(input_df, models.Incident.ABANDONED_VEHICLE)

        incidents = list()
        abandoned_vehicles = list()
        abandoned_vehicles_hashes = set()

        for row in input_df.itertuples(index=False):
            # print(row)

            if row.license_plate:
                abandoned_vehicle = models.AbandonedVehicle(license_plate=row.license_plate,
                                                            vehicle_color=row.vehicle_color,
                                                            vehicle_make_model=row.vehicle_make_model)
                obj_str = f'{str(row.license_plate or "")}{str(row.vehicle_color or "")}' \
                          f'{str(row.vehicle_make_model or "")}'
                vehicle_hash = hashlib.md5(obj_str.encode())
                if vehicle_hash.hexdigest() not in abandoned_vehicles_hashes:
                    abandoned_vehicles_hashes.add(vehicle_hash.hexdigest())
                    abandoned_vehicles.append(abandoned_vehicle)

            # TODO this could be a separate method because all incidents we import will have this chunk of code
            # Retrieve or create the current incident

            incident = models.Incident(creation_date=row.creation_date, status=self.get_status_type(row.status),
                                       completion_date=row.completion_date,
                                       service_request_number=row.service_request_number,
                                       type_of_service_request=row.type_of_service_request,
                                       current_activity=row.current_activity,
                                       most_recent_action=row.most_recent_action,
                                       street_address=row.street_address, zip_code=row.zip_code,
                                       zip_codes=row.zip_codes, x_coordinate=row.x_coordinate,
                                       y_coordinate=row.y_coordinate, ward=row.ward,
                                       wards=row.wards, historical_wards_03_15=row.historical_wards_03_15,
                                       police_district=row.police_district, community_area=row.community_area,
                                       community_areas=row.community_areas, ssa=row.ssa,
                                       census_tracts=row.census_tracts, latitude=row.latitude,
                                       longitude=row.longitude, location=row.location)
            incidents.append(incident)

        models.AbandonedVehicle.objects.bulk_create(abandoned_vehicles, batch_size=250000)
        models.Incident.objects.bulk_create(incidents, batch_size=250000)

        abandoned_vehicles_incidents = list()
        with transaction.atomic():
            for row in input_df.itertuples(index=False):
                try:
                    abandoned_vehicle = models.AbandonedVehicle.objects.get(license_plate=row.license_plate,
                                                                            vehicle_color=row.vehicle_color,
                                                                            vehicle_make_model=row.vehicle_make_model)

                except models.AbandonedVehicle.DoesNotExist:
                    continue

                incident = models.Incident.objects.get(creation_date=row.creation_date,
                                                       status=self.get_status_type(row.status),
                                                       completion_date=row.completion_date,
                                                       service_request_number=row.service_request_number,
                                                       type_of_service_request=row.type_of_service_request,
                                                       street_address=row.street_address)
                days_of_report_as_parked = row.days_of_report_as_parked
                if days_of_report_as_parked and days_of_report_as_parked > 1000000:
                    days_of_report_as_parked = 1000000
                abandoned_vehicle = models. \
                    AbandonedVehicleIncident(abandoned_vehicle=abandoned_vehicle, incident=incident,
                                             days_of_report_as_parked=days_of_report_as_parked)
                abandoned_vehicles_incidents.append(abandoned_vehicle)

        models.AbandonedVehicleIncident.objects.bulk_create(abandoned_vehicles_incidents, batch_size=250000)

    def import_garbage_carts(self, input_file: str):
        """Import the requests for garbage carts incidents

        :param input_file: he file from which to load the requests for garbage carts incidents.
        """
        self.stdout.write("Getting requests for garbage carts")

        input_df = pd.read_csv(input_file, sep=',').replace({np.nan: None})
        input_df.columns = ['creation_date', 'status', 'completion_date', 'service_request_number',
                            'type_of_service_request', 'number_of_carts', 'current_activity', 'most_recent_action',
                            'street_address', 'zip_code', 'x_coordinate', 'y_coordinate', 'ward', 'police_district',
                            'community_area', 'ssa', 'latitude', 'longitude', 'location', 'historical_wards_03_15',
                            'zip_codes', 'community_areas', 'census_tracts', 'wards']

        input_df = self.dataframe_normalization(input_df, models.Incident.GARBAGE_CART)

        incidents = list()

        for row in input_df.itertuples(index=False):
            # Retrieve or create the current incident
            incident = models.Incident(creation_date=row.creation_date, status=self.get_status_type(row.status),
                                       completion_date=row.completion_date,
                                       service_request_number=row.service_request_number,
                                       type_of_service_request=row.type_of_service_request,
                                       current_activity=row.current_activity,
                                       most_recent_action=row.most_recent_action,
                                       street_address=row.street_address, zip_code=row.zip_code,
                                       zip_codes=row.zip_codes, x_coordinate=row.x_coordinate,
                                       y_coordinate=row.y_coordinate, ward=row.ward,
                                       wards=row.wards, historical_wards_03_15=row.historical_wards_03_15,
                                       police_district=row.police_district, community_area=row.community_area,
                                       community_areas=row.community_areas, ssa=row.ssa,
                                       census_tracts=row.census_tracts, latitude=row.latitude,
                                       longitude=row.longitude, location=row.location)
            incidents.append(incident)

        models.Incident.objects.bulk_create(incidents, batch_size=250000)

        number_of_carts = list()
        with transaction.atomic():
            for row in input_df.itertuples(index=False):
                if row.number_of_carts:
                    incident = models.Incident.objects.get(creation_date=row.creation_date,
                                                           status=self.get_status_type(row.status),
                                                           completion_date=row.completion_date,
                                                           service_request_number=row.service_request_number,
                                                           type_of_service_request=row.type_of_service_request,
                                                           street_address=row.street_address)
                    carts = models.NumberOfCartsAndPotholes(incident=incident,
                                                            number_of_elements=row.number_of_carts if
                                                            row.number_of_carts < 1000000 else 1000000)
                    number_of_carts.append(carts)

        models.NumberOfCartsAndPotholes.objects.bulk_create(number_of_carts, batch_size=250000)

    def import_alley_lights_out_or_street_lights_all_out(self, input_file: str, street_lights: bool):
        """Import the requests for alley lights out or street lights all out (works the same for both of them) to the
        database.

        :param input_file: The file from which to load the requests for lights incidents.
        :param street_lights: Indicator if the method is called for street lights or not
        """
        if street_lights:
            self.stdout.write("Getting requests for street lights all out")
        else:
            self.stdout.write("Getting requests for alley lights out")

        input_df = pd.read_csv(input_file, sep=',').replace({np.nan: None})
        input_df.columns = ['creation_date', 'status', 'completion_date', 'service_request_number',
                            'type_of_service_request', 'street_address', 'zip_code', 'x_coordinate', 'y_coordinate',
                            'ward', 'police_district', 'community_area', 'latitude', 'longitude', 'location',
                            'historical_wards_03_15', 'zip_codes', 'community_areas', 'census_tracts', 'wards']

        if street_lights:
            input_df = self.dataframe_normalization(input_df, models.Incident.STREET_LIGHTS_ALL_OUT)
        else:
            input_df = self.dataframe_normalization(input_df, models.Incident.ALLEY_LIGHTS_OUT)

        incidents = list()

        for row in input_df.itertuples(index=False):
            incident = models.Incident(creation_date=row.creation_date, status=self.get_status_type(row.status),
                                       completion_date=row.completion_date,
                                       service_request_number=row.service_request_number,
                                       type_of_service_request=row.type_of_service_request,
                                       street_address=row.street_address, zip_code=row.zip_code,
                                       zip_codes=row.zip_codes, x_coordinate=row.x_coordinate,
                                       y_coordinate=row.y_coordinate, ward=row.ward, wards=row.wards,
                                       historical_wards_03_15=row.historical_wards_03_15,
                                       police_district=row.police_district, community_area=row.community_area,
                                       community_areas=row.community_areas, census_tracts=row.census_tracts,
                                       latitude=row.latitude, longitude=row.longitude, location=row.location)
            incidents.append(incident)

        models.Incident.objects.bulk_create(incidents, batch_size=250000)

    def import_street_lights_one_out(self, input_file: str):
        """Import the requests for street lights one out to the database.

        :param input_file: The file from which to load the requests for lights incidents.
        """
        self.stdout.write("Getting requests for street lights one out")
        input_df = pd.read_csv(input_file, sep=',').replace({np.nan: None})
        input_df.columns = ['creation_date', 'status', 'completion_date', 'service_request_number',
                            'type_of_service_request', 'street_address', 'zip_code', 'x_coordinate', 'y_coordinate',
                            'ward', 'police_district', 'community_area', 'latitude', 'longitude', 'location']

        input_df = self.dataframe_normalization(input_df, models.Incident.STREET_LIGHT_ONE_OUT)

        incidents = list()

        for row in input_df.itertuples(index=False):
            incident = models.Incident(creation_date=row.creation_date, status=self.get_status_type(row.status),
                                       completion_date=row.completion_date,
                                       service_request_number=row.service_request_number,
                                       type_of_service_request=row.type_of_service_request,
                                       street_address=row.street_address, zip_code=row.zip_code,
                                       x_coordinate=row.x_coordinate, y_coordinate=row.y_coordinate, ward=row.ward,
                                       police_district=row.police_district, community_area=row.community_area,
                                       latitude=row.latitude, longitude=row.longitude, location=row.location)
            incidents.append(incident)

        models.Incident.objects.bulk_create(incidents, batch_size=250000)

    @staticmethod
    def dataframe_normalization(df: pd.DataFrame, request_type: str) -> pd.DataFrame:
        """ Normalizes a given dataframe to a desired condition (removes duplicate rows, convert times to timezone
        aware etc.)

        :param df: A pandas dataframe
        :param request_type: The type of the incident
        :return:  The normalized dataframe
        """
        df = df.copy(deep=True)

        df = df.drop_duplicates()

        # Normalize type_of_service_request with the given
        df['type_of_service_request'] = df['type_of_service_request'].str.replace(r'.+', request_type)

        # Add UTC timezone to datetime fields
        df['creation_date'] = pd.to_datetime(df['creation_date'], errors='ignore')
        df['creation_date'] = df['creation_date'].dt.tz_localize("UTC")
        df['creation_date'] = df['creation_date'].astype(object).where(df['creation_date'].notnull(), None)
        df['completion_date'] = pd.to_datetime(df['completion_date'], errors='ignore')
        df['completion_date'] = df['completion_date'].dt.tz_localize("UTC")
        df['completion_date'] = df['completion_date'].astype(object).where(df['completion_date'].notnull(), None)

        return df

    @staticmethod
    def get_status_type(value: str) -> str:
        """

        :param value:
        :return:
        """
        for x in models.Incident.STATUS_TYPE_CHOICES:
            if x[1] == value:
                return x[0]
