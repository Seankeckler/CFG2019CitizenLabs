# pylint: disable=no-self-use

import re
from random import randint

from django.conf import settings

import bugsnag
import log

from elections import helpers, models

from ._bases import MichiganCrawler


class Command(MichiganCrawler):
    help = "Crawl the Michigan SOS website to discover precincts"

    def handle(self, start, limit, randomize, *_args, **_kwargs):
        log.init(reset=True)
        helpers.enable_requests_cache(settings.REQUESTS_CACHE_EXPIRE_AFTER)
        helpers.requests_cache.core.remove_expired_responses()
        try:
            self.discover_precincts(start, limit, randomize)
        except Exception as e:
            bugsnag.notify(e)
            raise e

    def discover_precincts(
        self,
        starting_mi_sos_precinct_id: int,
        max_precincts_count: int,
        randomly_skip_precincts: bool,
    ):
        election = (
            models.Election.objects.filter(active=True)
            .exclude(mi_sos_id=None)
            .first()
        )
        self.stdout.write(f"Crawling precincts for election: {election}")

        county_category = models.DistrictCategory.objects.get(name="County")
        jurisdiction_category = models.DistrictCategory.objects.get(
            name="Jurisdiction"
        )

        mi_sos_precinct_id = starting_mi_sos_precinct_id - 1
        misses = 0
        while misses < 10:
            if randomly_skip_precincts and mi_sos_precinct_id > 0:
                step = randint(1, 250)
            else:
                step = 1
            mi_sos_precinct_id += step

            # Stop early if requested
            count = models.Precinct.objects.count()
            if max_precincts_count and count >= max_precincts_count:
                self.stdout.write(f"Stopping at {count} precinct(s)")
                return

            # Fetch ballot website
            website, created = models.BallotWebsite.objects.get_or_create(
                mi_sos_election_id=election.mi_sos_id,
                mi_sos_precinct_id=mi_sos_precinct_id,
            )
            if created:
                self.stdout.write(f'Added website: {website}')
            elif website.valid:
                log.debug(f'Ballot already scraped: {website}')
                if misses:
                    self.stdout.write(f'ID={mi_sos_precinct_id}, Misses=0')
                misses = 0
                continue
            elif not website.stale(fuzz=0.5):
                log.debug(f'Invalid ballot already scraped: {website}')
                misses += 1
                self.stdout.write(f'ID={mi_sos_precinct_id}, Misses={misses}')
                continue

            # Validate ballot website
            website.fetch()
            website.save()
            if website.valid:
                if misses:
                    self.stdout.write(f'ID={mi_sos_precinct_id}, Misses: 0')
                misses = 0
            else:
                log.warn(f'Invalid ballot website: {website}')
                misses += 1
                self.stdout.write(f'ID={mi_sos_precinct_id}, Misses: {misses}')
                continue

            # Parse county
            match = re.search(
                r'(?P<county_name>[^>]+) County, Michigan', website.mi_sos_html
            )
            assert match, f'Could not find county name: {website.mi_sos_url}'
            county_name = match.group('county_name')

            # Parse jurisdiction, ward, and number
            jurisdiction_name, ward, number = self.parse_jurisdiction(
                website.mi_sos_html, website.mi_sos_url
            )

            # Add county
            county, created = models.District.objects.get_or_create(
                category=county_category, name=county_name
            )
            if created:
                self.stdout.write(f'Added county: {county}')
            else:
                self.stdout.write(f'Matched county: {county}')

            # Add jurisdiction
            jurisdiction, created = models.District.objects.get_or_create(
                category=jurisdiction_category, name=jurisdiction_name
            )
            if created:
                self.stdout.write(f'Added jurisdiction: {jurisdiction}')
            else:
                self.stdout.write(f'Matched jurisdiction: {jurisdiction}')

            # Add precinct
            precinct, created = models.Precinct.objects.get_or_create(
                county=county,
                jurisdiction=jurisdiction,
                ward=ward,
                number=number,
                defaults=dict(mi_sos_id=mi_sos_precinct_id),
            )
            if created:
                self.stdout.write(f'Added precinct: {precinct}')
                website.source = True
                website.save()
            elif precinct.mi_sos_id == mi_sos_precinct_id:
                self.stdout.write(f'Matched precinct: {precinct}')
            elif not precinct.mi_sos_id:
                self.stdout.write(f'Updated precinct: {precinct}')
                precinct.mi_sos_id = mi_sos_precinct_id
                precinct.save()
                website.source = True
                website.save()
            else:
                log.warn(f'Duplicate precinct: {website}')
                precinct.delete()
                website.source = False
                website.save()
                continue

            # Add ballot
            ballot, created = models.Ballot.objects.update_or_create(
                election=election,
                precinct=precinct,
                defaults=dict(website=website),
            )
            if created:
                self.stdout.write(f'Added ballot: {ballot}')
            else:
                self.stdout.write(f'Updated ballot: {ballot}')

    @staticmethod
    def parse_jurisdiction(html, url):
        match = None
        for pattern in [
            r'(?P<jurisdiction_name>[^>]+), Ward (?P<ward>\d+) Precinct (?P<precinct>\d+)<',
            r'(?P<jurisdiction_name>[^>]+),  Precinct (?P<precinct>\d+[A-Z]?)<',
            r'(?P<jurisdiction_name>[^>]+), Ward (?P<ward>\d+) <',
        ]:
            match = re.search(pattern, html)
            if match:
                break
        assert match, f'Unable to find precinct information: {url}'

        jurisdiction_name = match.group('jurisdiction_name')

        try:
            ward = match.group('ward')
        except IndexError:
            ward = ''

        try:
            precinct = match.group('precinct')
        except IndexError:
            precinct = ''

        return (jurisdiction_name, ward, precinct)