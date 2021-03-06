# coding: utf8

from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from remote_peering import models

class Command(BaseCommand):
    """Import ixps from peeringdb"""

    def add_arguments(self, parser):
        parser.add_argument('--file', '-f', required=True)


    def _parse_location(self, attribute):
        """Extract location attributes from data"""
        tokens = [t.strip() for t in attribute.split(',')]
        if len(tokens) != 3:
            return None

        location = {
            'city': tokens[0],
            'country': tokens[1],
            'continent': tokens[2],
        }
        return location

    def _parse_locations(self, attribute):
        """Extract locations from row"""
        locations_data = attribute.split('|')
        locations = [self._parse_location(l) for l in locations_data]
        return locations


    def _parse_row(self, row):
        """Attributes are tabseparated;
           PeeringDB ID \t IXP \t Location
           Location := CSV(city, country, continent)
        """
        attributes = row.split("\t")
        result = {
            "ixp": {
                "peeringdb_id": int(attributes[0]),
                "name": attributes[1],
            },
            "locations": self._parse_locations(attributes[2]),
        }
        return result

    def _read_export(self, filename):
        """Read export, extract data"""
        with open(filename) as f:
            lines = f.readlines()
            data = (self._parse_row(l.decode('utf8')) for l in lines)
            return data


    def _import_location(self, location_data):
        """Create location"""
        if not location_data:
            return None

        location, _ = models.Location.objects.get_or_create(**location_data)
        return location


    def _import_ixp(self, row):
        """Create IXP and include location"""
        ixp, _ = models.Ixp.objects.get_or_create(**row['ixp'])

        # Assign locations
        for loc in row['locations']:
            location = self._import_location(loc)
            if location:
                ixp.locations.add(location)

        return ixp


    def handle(self, *args, **options):
        """Perform IXP import"""
        filename = options['file']

        rows = self._read_export(filename)
        for row in rows:
            # Import into database
            try:
                ixp = self._import_ixp(row)
                print("Imported {}".format(ixp.name))
            except Exception as e:
                print("Import failed for {}".format(row['ixp']['name']))
                print(e)

