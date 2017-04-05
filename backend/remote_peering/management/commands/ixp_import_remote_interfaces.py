
from django.core.management.base import BaseCommand
from django.utils import timezone

import json

from remote_peering import models

class Command(BaseCommand):
    """
    Import remote interface file
    """
    help = 'Imports a remote interfaces file'

    def add_arguments(self, parser):
        parser.add_argument('--file', '-f', required=True)


    def _read_interfaces_file(self, filename):
        """Read interfaces file"""
        with open(filename) as f:
            line = f.readlines()
            return (json.loads(l) for l in line)


    def _parse_filename(self, filename):
        tokens = filename.split('.')
        if len(tokens) < 4:
            raise Exception("Filename must follow: <name>.<IXP>.<date:yyyymmdd>")
        return tokens


    def _filename_to_ixp(self, filename):
        """Extracts ixp from filename"""
        tokens = self._parse_filename(filename)
        return tokens[-3]


    def _filename_to_date(self, filename):
        tokens = self._parse_filename(filename)
        date = tokens[-2]

        # Create timezone aware datetime
        return timezone.datetime(int(date[:4]),
                                 int(date[4:6]),
                                 int(date[6:]),
                                 tzinfo=timezone.utc)


    def _import_location(self, row):
        """Get location data from row, create objects"""
        location, _ = models.Location.objects.get_or_create(city=row['city'],
                                                            country=row['country'],
                                                            continent=row['continent'])
        return location


    def _import_ixp(self, row):
        """Get or create the required IXP"""


    def _import_data(self, row):
        """Store row in database, create objects if required"""
        location = self._import_location(row)
        ixp = self._import_ixp(row, location)


    def handle(self, *args, **options):
        """Perform import of file"""
        filename = options['file']
        try:
            ixp = self._filename_to_ixp(filename)
            date = self._filename_to_date(filename)
        except Exception as e:
            print("Could not load file: {}".format(filename))
            print(e)
            return

        print("Importing: {} for IXP: {}, Date: {}".format(filename,
                                                           ixp,
                                                           date))
        data = self._read_interfaces_file(options['file'])
        for row in data:
            self._import_data(row)