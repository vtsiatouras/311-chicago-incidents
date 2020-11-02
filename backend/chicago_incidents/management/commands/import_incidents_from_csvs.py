import time

from django.core.management.base import BaseCommand, CommandParser
import pandas as pd

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
            else:
                self.stdout.write(f"File cannot be processed, skipping.")

        end = time.time()
        self.stdout.write(f"Finished importing competing products prices data data, took {(end - start):.2f} seconds")

    def import_abandoned_vehicles(self, input_file: str):
        """Import the requests for abandoned vehicles to the database.

        :param input_file: The file from which to load the requests for abandoned vehicles.
        """
        self.stdout.write("Getting requests for abandoned vehicles")
        input_df = pd.read_csv(input_file)
        for row in input_df.itertuples(index=False):
            print(row)
