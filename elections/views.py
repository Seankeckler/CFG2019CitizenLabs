from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.response import Response

from . import models, serializers


class RegistrationViewSet(viewsets.ViewSetMixin, generics.ListAPIView):
    """Status of a particular voter's registration."""

    queryset = models.Voter.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['first_name', 'last_name', 'zip_code', 'birth_date']

    def list(self, request):  # pylint: disable=arguments-differ
        input_serializer = serializers.VoterSerializer(
            data=request.query_params
        )
        input_serializer.is_valid(raise_exception=True)
        voter = models.Voter(**input_serializer.validated_data)

        registration_status = voter.fetch_registration_status()

        output_serializer = serializers.RegistrationStatusSerializer(
            registration_status, context={'request': request}
        )
        return Response([output_serializer.data])


class DistrictCategoryViewSet(
    viewsets.ViewSetMixin, generics.RetrieveAPIView, generics.ListAPIView
):
    """Types of regions that bound ballot items."""

    # http_method_names = ["get"]
    queryset = models.DistrictCategory.objects.all()
    serializer_class = serializers.DistrictCategorySerializer


class DistrictViewSet(
    viewsets.ViewSetMixin, generics.RetrieveAPIView, generics.ListAPIView
):
    """Districts bound to ballot items."""

    queryset = models.District.objects.all()
    serializer_class = serializers.DistrictSerializer
