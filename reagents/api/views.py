from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from authentication.api.permissions import IsAdminOrReadOnly
from reagents.models import Container
from reagents.serializer import ContainerSerializer


class ContainerModelViewSet(ModelViewSet):
    serializer_class = ContainerSerializer
    queryset = Container.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["precursor"]


class ReagentsViewSet(APIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["precursor"]

    def get(self, request):
        summary = Container.objects.values("cas", "qualification", "name", "formula", "density", "precursor").annotate(
            total_volume=Sum("volume"), total_mass=Sum("mass")
        )
        data = [
            {
                "name": item["name"],
                "formula": item["formula"],
                "mass": item["total_mass"],
                "volume": item["total_volume"],
                "density": item["density"],
                "precursor": item["precursor"],
                "cas": item["cas"],
                "qualification": item["qualification"],
            }
            for item in summary
        ]

        return Response(data, status=status.HTTP_200_OK)
