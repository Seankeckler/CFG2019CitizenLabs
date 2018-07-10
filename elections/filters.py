from django_filters import rest_framework as filters

from . import models


DjangoFilterBackend = filters.DjangoFilterBackend


class PollFilter(filters.FilterSet):

    # ID lookup
    county_id = filters.NumberFilter(name='county')
    jurisdiction_id = filters.NumberFilter(name='jurisdiction')

    # Value lookup
    county = filters.CharFilter(name='county__name')
    jurisdiction = filters.CharFilter(name='jurisdiction__name')
    ward = filters.CharFilter(name='ward')
    precinct = filters.CharFilter(name='precinct')

    class Meta:
        model = models.Poll
        fields = [
            # ID lookup
            'county_id',
            'jurisdiction_id',
            # Value lookup
            'county',
            'jurisdiction',
            'ward',
            'precinct',
        ]


class BallotFilter(filters.FilterSet):

    # ID lookup
    poll_id = filters.NumberFilter(name='poll')

    # Value lookup
    county = filters.CharFilter(name='poll__county__name')
    jurisdiction = filters.CharFilter(name='poll__jurisdiction__name')
    ward = filters.CharFilter(name='poll__ward')
    precinct = filters.CharFilter(name='poll__precinct')

    class Meta:
        model = models.Ballot
        fields = [
            # ID lookup
            'poll_id',
            # Value lookup
            'county',
            'jurisdiction',
            'ward',
            'precinct',
        ]
