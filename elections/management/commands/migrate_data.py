# pylint: disable=no-self-use

import sys
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

import log

from elections.models import District, DistrictCategory, Election, Party


class Command(BaseCommand):
    help = "Initialize contants and migrate data between existing models"

    def handle(self, verbosity: int, **_kwargs):
        log.init(verbosity=verbosity if '-v' in sys.argv else 2)

        self.initialize_parties()
        self.initialize_districts()

        self.update_elections()

    def initialize_parties(self):
        for name, color in [
            # Placeholders
            ("Nonpartisan", '#999'),
            ("No Party Affiliation", '#999'),
            # Parties
            ("Democratic", '#3333FF'),
            ("Green", '#00A95C'),
            ("Libertarian", '#ECC850'),
            ("Natural Law", '#FFF7D6'),
            ("Republican", '#E81B23'),
            ("U.S. Taxpayers", '#A356DE'),
            ("Working Class", '#A30000'),
        ]:
            party, created = Party.objects.update_or_create(
                name=name, defaults=dict(color=color)
            )
            if created:
                log.info(f'Added party: {party}')

    def initialize_districts(self):
        state, created = DistrictCategory.objects.get_or_create(name="State")
        if created:
            log.info(f'Added district category: {state}')

        for name in [
            # State
            "County",
            "Jurisdiction",
            "Precinct",
            # Local
            "City",
            "District Library",
            "Local School",
            "Intermediate School",
            "Township",
            "Metropolitan",
            "Village",
            "Authority",
            "Library",
        ]:
            category, created = DistrictCategory.objects.get_or_create(name=name)
            if created:
                log.info(f'Added district category: {category}')

        michigan, created = District.objects.get_or_create(
            category=state, name="Michigan"
        )
        if created:
            log.info(f'Added district: {michigan}')

    def update_elections(self):
        for election in Election.objects.filter(active=True):
            age = timezone.now() - timedelta(weeks=3)
            if election.date < age.date():
                log.info(f'Deactivating election: {election}')
                election.active = False
                election.save()
