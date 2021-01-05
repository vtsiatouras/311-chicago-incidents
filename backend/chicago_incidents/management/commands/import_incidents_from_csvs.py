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
                self.import_garbage_carts_or_potholes(input_file, garbage_carts=True)
            elif input_file.endswith('graffiti-removal.csv'):
                self.import_graffiti_removal(input_file)
            elif input_file.endswith('pot-holes-reported.csv'):
                self.import_garbage_carts_or_potholes(input_file, garbage_carts=False)
            elif input_file.endswith('rodent-baiting.csv'):
                self.import_rodent_baiting(input_file)
            elif input_file.endswith('sanitation-code-complaints.csv'):
                self.import_sanitation_complaints(input_file)
            elif input_file.endswith('tree-debris.csv'):
                self.import_tree_incidents(input_file, debris=True)
            elif input_file.endswith('tree-trims.csv'):
                self.import_tree_incidents(input_file, debris=False)
            elif input_file.endswith('street-lights-all-out.csv'):
                self.import_alley_lights_out_or_street_lights_all_out(input_file, street_lights=True)
            elif input_file.endswith('street-lights-one-out.csv'):
                self.import_street_lights_one_out(input_file)
            else:
                self.stdout.write(f"File '{input_file}' cannot be processed, skipping.")

        end = time.time()
        self.stdout.write(f"Finished importing datasets, took {(end - start):.2f} seconds")

    def import_abandoned_vehicles(self, input_file: str):
        """ Import the requests for abandoned abandoned_vehicles to the database.

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
        activity_incidents = list()
        abandoned_vehicles = list()
        abandoned_vehicles_dict = dict()
        abandoned_vehicles_incidents = list()
        with transaction.atomic():
            for row in input_df.itertuples(index=False):
                # Retrieve or create the current incident
                incident = models.Incident(creation_date=row.creation_date, status=self.get_status_type(row.status),
                                           completion_date=row.completion_date,
                                           service_request_number=row.service_request_number,
                                           type_of_service_request=row.type_of_service_request,
                                           street_address=row.street_address, zip_code=row.zip_code,
                                           zip_codes=row.zip_codes, x_coordinate=row.x_coordinate,
                                           y_coordinate=row.y_coordinate, ward=row.ward,
                                           wards=row.wards, historical_wards_03_15=row.historical_wards_03_15,
                                           police_district=row.police_district, community_area=row.community_area,
                                           community_areas=row.community_areas, ssa=row.ssa,
                                           census_tracts=row.census_tracts, latitude=row.latitude,
                                           longitude=row.longitude, location=row.location)
                incidents.append(incident)

                if any([row.license_plate, row.vehicle_color, row.vehicle_make_model]):
                    abandoned_vehicle = models.AbandonedVehicle(license_plate=row.license_plate,
                                                                vehicle_color=row.vehicle_color,
                                                                vehicle_make_model=row.vehicle_make_model)

                    # In order to avoid inserting duplicate abandoned cars without querying the database
                    # we use in memory hashing from the dataframe values
                    obj_str = f'{str(row.license_plate or "")}{str(row.vehicle_color or "")}' \
                              f'{str(row.vehicle_make_model or "")}'
                    vehicle_hash = hashlib.md5(obj_str.encode()).hexdigest()
                    if vehicle_hash not in abandoned_vehicles_dict:
                        abandoned_vehicles_dict.update({vehicle_hash: abandoned_vehicle})
                        abandoned_vehicles.append(abandoned_vehicle)

                    days_of_report_as_parked = row.days_of_report_as_parked
                    if days_of_report_as_parked and int(days_of_report_as_parked) > 1000000:
                        days_of_report_as_parked = 1000000
                    abandoned_vehicles_incident = models. \
                        AbandonedVehicleIncident(abandoned_vehicle=abandoned_vehicles_dict[vehicle_hash],
                                                 incident=incident,
                                                 days_of_report_as_parked=days_of_report_as_parked)
                    abandoned_vehicles_incidents.append(abandoned_vehicles_incident)

                # Get the activity of the incident
                activity, _ = self.import_activity(row)
                if activity:
                    activity_incident = models.ActivityIncident(activity=activity, incident=incident)
                    activity_incidents.append(activity_incident)

        models.AbandonedVehicle.objects.bulk_create(abandoned_vehicles, batch_size=250000)
        models.Incident.objects.bulk_create(incidents, batch_size=250000)

        for activity_incident in activity_incidents:
            activity_incident.incident_id = activity_incident.incident.id
            activity_incident.activity_id = activity_incident.activity.id
        for abandoned_vehicle_incident in abandoned_vehicles_incidents:
            abandoned_vehicle_incident.incident_id = abandoned_vehicle_incident.incident.id
            abandoned_vehicle_incident.abandoned_vehicle_id = abandoned_vehicle_incident.abandoned_vehicle.id

        models.ActivityIncident.objects.bulk_create(activity_incidents, batch_size=250000)
        models.AbandonedVehicleIncident.objects.bulk_create(abandoned_vehicles_incidents, batch_size=250000)

    def import_garbage_carts_or_potholes(self, input_file: str, garbage_carts: bool):
        """ Import the requests for garbage carts incidents

        :param input_file: The file from which to load the requests for garbage carts incidents.
        :param garbage_carts: Indicator if the method is called for garbage carts or not
        """
        if garbage_carts:
            self.stdout.write("Getting requests for garbage carts")
        else:
            self.stdout.write("Getting requests for potholes")

        input_df = pd.read_csv(input_file, sep=',').replace({np.nan: None})

        if garbage_carts:
            input_df.columns = ['creation_date', 'status', 'completion_date', 'service_request_number',
                                'type_of_service_request', 'number_of_elements', 'current_activity',
                                'most_recent_action', 'street_address', 'zip_code', 'x_coordinate', 'y_coordinate',
                                'ward', 'police_district', 'community_area', 'ssa', 'latitude', 'longitude',
                                'location', 'historical_wards_03_15', 'zip_codes', 'community_areas',
                                'census_tracts', 'wards']
            input_df = self.dataframe_normalization(input_df, models.Incident.GARBAGE_CART)
        else:
            input_df.columns = ['creation_date', 'status', 'completion_date', 'service_request_number',
                                'type_of_service_request', 'current_activity', 'most_recent_action',
                                'number_of_elements', 'street_address', 'zip_code', 'x_coordinate', 'y_coordinate',
                                'ward', 'police_district', 'community_area', 'ssa', 'latitude', 'longitude',
                                'location', 'historical_wards_03_15', 'zip_codes', 'community_areas',
                                'census_tracts', 'wards']
            input_df = self.dataframe_normalization(input_df, models.Incident.POT_HOLE)

        incidents = list()
        number_of_elements = list()
        activity_incidents = list()
        with transaction.atomic():
            for row in input_df.itertuples(index=False):
                incident = models.Incident(creation_date=row.creation_date, status=self.get_status_type(row.status),
                                           completion_date=row.completion_date,
                                           service_request_number=row.service_request_number,
                                           type_of_service_request=row.type_of_service_request,
                                           street_address=row.street_address, zip_code=row.zip_code,
                                           zip_codes=row.zip_codes, x_coordinate=row.x_coordinate,
                                           y_coordinate=row.y_coordinate, ward=row.ward,
                                           wards=row.wards, historical_wards_03_15=row.historical_wards_03_15,
                                           police_district=row.police_district, community_area=row.community_area,
                                           community_areas=row.community_areas, ssa=row.ssa,
                                           census_tracts=row.census_tracts, latitude=row.latitude,
                                           longitude=row.longitude, location=row.location)
                incidents.append(incident)

                if row.number_of_elements:
                    number_of_elements_to_int = row.number_of_elements
                    if int(number_of_elements_to_int) > 1000000:
                        number_of_elements_to_int = 1000000
                    elements = models.NumberOfCartsAndPotholes(incident=incident,
                                                               number_of_elements=number_of_elements_to_int)
                    number_of_elements.append(elements)

                # Get the activity of the incident
                activity, _ = self.import_activity(row)
                if activity:
                    activity_incident = models.ActivityIncident(activity=activity, incident=incident)
                    activity_incidents.append(activity_incident)

        models.Incident.objects.bulk_create(incidents, batch_size=250000)

        for activity_incident in activity_incidents:
            activity_incident.incident_id = activity_incident.incident.id
            activity_incident.activity_id = activity_incident.activity.id
        for element in number_of_elements:
            element.incident_id = element.incident.id

        models.NumberOfCartsAndPotholes.objects.bulk_create(number_of_elements, batch_size=250000)
        models.ActivityIncident.objects.bulk_create(activity_incidents, batch_size=250000)

    def import_graffiti_removal(self, input_file: str):
        """ Import the requests for graffiti removal incidents

        :param input_file: The file from which to load the requests for graffiti removal incidents.
        """
        self.stdout.write("Getting requests for graffiti removal")

        input_df = pd.read_csv(input_file, sep=',').replace({np.nan: None})
        input_df.columns = ['creation_date', 'status', 'completion_date', 'service_request_number',
                            'type_of_service_request', 'surface', 'graffiti_location', 'street_address',
                            'zip_code', 'x_coordinate', 'y_coordinate', 'ward', 'police_district', 'community_area',
                            'ssa', 'latitude', 'longitude', 'location', 'historical_wards_03_15', 'zip_codes',
                            'community_areas', 'census_tracts', 'wards']

        input_df = self.dataframe_normalization(input_df, models.Incident.GRAFFITI)

        incidents = list()
        graffiti_list = list()
        graffiti_dict = dict()
        graffiti_incidents = list()
        for row in input_df.itertuples(index=False):
            incident = models.Incident(creation_date=row.creation_date, status=self.get_status_type(row.status),
                                       completion_date=row.completion_date,
                                       service_request_number=row.service_request_number,
                                       type_of_service_request=row.type_of_service_request,
                                       street_address=row.street_address, zip_code=row.zip_code,
                                       zip_codes=row.zip_codes, x_coordinate=row.x_coordinate,
                                       y_coordinate=row.y_coordinate, ward=row.ward,
                                       wards=row.wards, historical_wards_03_15=row.historical_wards_03_15,
                                       police_district=row.police_district, community_area=row.community_area,
                                       community_areas=row.community_areas, ssa=row.ssa,
                                       census_tracts=row.census_tracts, latitude=row.latitude,
                                       longitude=row.longitude, location=row.location)
            incidents.append(incident)

            if any([row.surface, row.graffiti_location]):
                graffiti = models.Graffiti(surface=row.surface, location=row.graffiti_location)
                obj_str = f'{str(row.surface or "")}{str(row.graffiti_location or "")}'
                graffiti_hash = hashlib.md5(obj_str.encode()).hexdigest()
                if graffiti_hash not in graffiti_dict:
                    graffiti_dict.update({graffiti_hash: graffiti})
                    graffiti_list.append(graffiti)

                graffiti_incident = models.GraffitiIncident(graffiti=graffiti_dict[graffiti_hash], incident=incident)
                graffiti_incidents.append(graffiti_incident)

        models.Incident.objects.bulk_create(incidents, batch_size=250000)
        models.Graffiti.objects.bulk_create(graffiti_list, batch_size=250000)

        for graffiti_incident in graffiti_incidents:
            graffiti_incident.incident_id = graffiti_incident.incident.id
            graffiti_incident.graffiti_id = graffiti_incident.graffiti.id

        models.GraffitiIncident.objects.bulk_create(graffiti_incidents, batch_size=250000)

    def import_rodent_baiting(self, input_file: str):
        """ Import the requests for rodent baiting incidents to the database

        :param input_file: The file from which to load the requests for rodent baiting incidents.
        """
        self.stdout.write("Getting requests for rodent baiting")

        input_df = pd.read_csv(input_file, sep=',').replace({np.nan: None})
        input_df.columns = ['creation_date', 'status', 'completion_date', 'service_request_number',
                            'type_of_service_request', 'number_of_premises_baited', 'number_of_premises_w_garbage',
                            'number_of_premises_w_rats', 'current_activity', 'most_recent_action', 'street_address',
                            'zip_code', 'x_coordinate', 'y_coordinate', 'ward', 'police_district', 'community_area',
                            'latitude', 'longitude', 'location', 'historical_wards_03_15', 'zip_codes',
                            'community_areas', 'census_tracts', 'wards']

        input_df = self.dataframe_normalization(input_df, models.Incident.RODENT_BAITING)

        incidents = list()
        rodent_baiting_premises = list()
        activity_incidents = list()
        with transaction.atomic():
            for row in input_df.itertuples(index=False):
                incident = models.Incident(creation_date=row.creation_date, status=self.get_status_type(row.status),
                                           completion_date=row.completion_date,
                                           service_request_number=row.service_request_number,
                                           type_of_service_request=row.type_of_service_request,
                                           street_address=row.street_address, zip_code=row.zip_code,
                                           zip_codes=row.zip_codes, x_coordinate=row.x_coordinate,
                                           y_coordinate=row.y_coordinate, ward=row.ward,
                                           wards=row.wards, historical_wards_03_15=row.historical_wards_03_15,
                                           police_district=row.police_district, community_area=row.community_area,
                                           community_areas=row.community_areas, census_tracts=row.census_tracts,
                                           latitude=row.latitude, longitude=row.longitude, location=row.location)
                incidents.append(incident)

                if any([row.number_of_premises_baited, row.number_of_premises_w_garbage,
                        row.number_of_premises_w_rats]):
                    rodent_baiting = models. \
                        RodentBaitingPremises(number_of_premises_baited=row.number_of_premises_baited,
                                              number_of_premises_w_garbage=row.number_of_premises_w_garbage,
                                              number_of_premises_w_rats=row.number_of_premises_w_rats,
                                              incident=incident)
                    rodent_baiting_premises.append(rodent_baiting)

                # Get the activity of the incident
                activity, _ = self.import_activity(row)
                if activity:
                    activity_incident = models.ActivityIncident(activity=activity, incident=incident)
                    activity_incidents.append(activity_incident)

        models.Incident.objects.bulk_create(incidents, batch_size=250000)

        for activity_incident in activity_incidents:
            activity_incident.incident_id = activity_incident.incident.id
            activity_incident.activity_id = activity_incident.activity.id
        for premise in rodent_baiting_premises:
            premise.incident_id = premise.incident.id

        models.ActivityIncident.objects.bulk_create(activity_incidents, batch_size=250000)
        models.RodentBaitingPremises.objects.bulk_create(rodent_baiting_premises, batch_size=250000)

    def import_sanitation_complaints(self, input_file: str):
        """ Import the requests for sanitation code complaints requests to tha database.

        :param input_file: The file from which to load the requests for sanitation code violations.
        """
        self.stdout.write("Getting requests for sanitation code complaints")

        input_df = pd.read_csv(input_file, sep=',').replace({np.nan: None})
        input_df.columns = ['creation_date', 'status', 'completion_date', 'service_request_number',
                            'type_of_service_request', 'nature_of_code_violation', 'street_address',
                            'zip_code', 'x_coordinate', 'y_coordinate', 'ward', 'police_district', 'community_area',
                            'latitude', 'longitude', 'location', 'historical_wards_03_15', 'zip_codes',
                            'community_areas', 'census_tracts', 'wards']

        input_df = self.dataframe_normalization(input_df, models.Incident.SANITATION_CODE)

        incidents = list()
        code_violations = list()
        code_violations_dict = dict()
        sanitation_code_incidents = list()
        for row in input_df.itertuples(index=False):
            incident = models.Incident(creation_date=row.creation_date, status=self.get_status_type(row.status),
                                       completion_date=row.completion_date,
                                       service_request_number=row.service_request_number,
                                       type_of_service_request=row.type_of_service_request,
                                       street_address=row.street_address, zip_code=row.zip_code,
                                       zip_codes=row.zip_codes, x_coordinate=row.x_coordinate,
                                       y_coordinate=row.y_coordinate, ward=row.ward,
                                       wards=row.wards, historical_wards_03_15=row.historical_wards_03_15,
                                       police_district=row.police_district, community_area=row.community_area,
                                       community_areas=row.community_areas, census_tracts=row.census_tracts,
                                       latitude=row.latitude, longitude=row.longitude, location=row.location)
            incidents.append(incident)

            if row.nature_of_code_violation:
                code_violation = models.SanitationCodeViolation(nature_of_code_violation=row.nature_of_code_violation)
                obj_str = f'{str(row.nature_of_code_violation or "")}'
                code_violation_hash = hashlib.md5(obj_str.encode()).hexdigest()
                if code_violation_hash not in code_violations_dict:
                    code_violations_dict.update({code_violation_hash: code_violation})
                    code_violations.append(code_violation)

                sanitation_code_incident = models. \
                    SanitationCodeViolationIncident(sanitation_code_violation=code_violations_dict[code_violation_hash],
                                                    incident=incident)
                sanitation_code_incidents.append(sanitation_code_incident)

        models.SanitationCodeViolation.objects.bulk_create(code_violations, batch_size=250000)
        models.Incident.objects.bulk_create(incidents, batch_size=250000)

        for code_incident in sanitation_code_incidents:
            code_incident.incident_id = code_incident.incident.id
            code_incident.sanitation_code_violation_id = code_incident.sanitation_code_violation.id

        models.SanitationCodeViolationIncident.objects.bulk_create(sanitation_code_incidents, batch_size=250000)

    def import_tree_incidents(self, input_file: str, debris: bool):
        """ Import the requests that refer to tree incidents (debris & trims) to the database.

        :param input_file: The file from which to load the requests for tree incidents.
        :param debris: Indicator if the method is called for tree debris or not
        """
        if debris:
            self.stdout.write("Getting requests for tree debris")
        else:
            self.stdout.write("Getting requests for tree trims")

        input_df = pd.read_csv(input_file, sep=',').replace({np.nan: None})

        if debris:
            input_df.columns = ['creation_date', 'status', 'completion_date', 'service_request_number',
                                'type_of_service_request', 'tree_location', 'current_activity',
                                'most_recent_action', 'street_address', 'zip_code', 'x_coordinate', 'y_coordinate',
                                'ward', 'police_district', 'community_area', 'latitude', 'longitude',
                                'location', 'historical_wards_03_15', 'zip_codes', 'community_areas',
                                'census_tracts', 'wards']
            input_df = self.dataframe_normalization(input_df, models.Incident.TREE_DEBRIS)
        else:
            input_df.columns = ['creation_date', 'status', 'completion_date', 'service_request_number',
                                'type_of_service_request', 'tree_location', 'street_address', 'zip_code',
                                'x_coordinate', 'y_coordinate', 'ward', 'police_district', 'community_area',
                                'latitude', 'longitude', 'location', 'historical_wards_03_15', 'zip_codes',
                                'community_areas', 'census_tracts', 'wards']
            input_df = self.dataframe_normalization(input_df, models.Incident.TREE_TRIM)

        incidents = list()
        trees_incidents = list()
        activity_incidents = list()
        with transaction.atomic():
            for row in input_df.itertuples(index=False):
                incident = models.Incident(creation_date=row.creation_date, status=self.get_status_type(row.status),
                                           completion_date=row.completion_date,
                                           service_request_number=row.service_request_number,
                                           type_of_service_request=row.type_of_service_request,
                                           street_address=row.street_address, zip_code=row.zip_code,
                                           zip_codes=row.zip_codes, x_coordinate=row.x_coordinate,
                                           y_coordinate=row.y_coordinate, ward=row.ward,
                                           wards=row.wards, historical_wards_03_15=row.historical_wards_03_15,
                                           police_district=row.police_district, community_area=row.community_area,
                                           community_areas=row.community_areas, census_tracts=row.census_tracts,
                                           latitude=row.latitude, longitude=row.longitude, location=row.location)
                incidents.append(incident)

                if row.location:
                    # In memory hashing with dataframe values can't be applied here because this importer runs more
                    # than one times (tree debris & tree trims)
                    tree, _ = models.Tree.objects.get_or_create(location=row.tree_location)
                    tree_incident = models.TreeIncident(tree=tree, incident=incident)
                    trees_incidents.append(tree_incident)

                # Get the activity of the incident
                activity, _ = self.import_activity(row)
                if activity:
                    activity_incident = models.ActivityIncident(activity=activity, incident=incident)
                    activity_incidents.append(activity_incident)

        models.Incident.objects.bulk_create(incidents, batch_size=250000)

        for activity_incident in activity_incidents:
            activity_incident.incident_id = activity_incident.incident.id
            activity_incident.activity_id = activity_incident.activity.id
        for tree_incident in trees_incidents:
            tree_incident.incident_id = tree_incident.incident.id
            tree_incident.tree_id = tree_incident.tree.id

        models.TreeIncident.objects.bulk_create(trees_incidents, batch_size=250000)

    def import_alley_lights_out_or_street_lights_all_out(self, input_file: str, street_lights: bool):
        """ Import the requests for alley lights out or street lights all out (works the same for both of them) to the
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
        """ Import the requests for street lights one out to the database.

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
    def import_activity(row: pd.DataFrame) -> tuple:
        """ This method creates Activity objects in order to store them to the db

        :param row: The row we read from the csv
        :return: The Activity object
        """
        try:
            current_activity = row.current_activity
        except AttributeError:
            current_activity = None
        try:
            most_recent_action = row.most_recent_action
        except AttributeError:
            most_recent_action = None
        if any([current_activity, most_recent_action]):
            # Naively just get or create the activity
            return models.Activity.objects.get_or_create(current_activity=current_activity,
                                                         most_recent_action=most_recent_action)
        else:
            return None, None

    @staticmethod
    def dataframe_normalization(df: pd.DataFrame, request_type: str) -> pd.DataFrame:
        """ Normalizes a given dataframe to a desired condition (removes duplicate rows, convert times to timezone
        aware etc.)

        :param df: A pandas dataframe
        :param request_type: The type of the incident
        :return:  The normalized dataframe
        """
        df = df.copy(deep=True)

        df = df.drop_duplicates(['creation_date', 'status', 'completion_date', 'service_request_number',
                                 'type_of_service_request', 'street_address', 'zip_code'], keep='last')

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
