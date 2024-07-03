from django.db.models import Sum
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from reagents.serializer import ContainerSerializer
from reagents.models import Container


class ContainerModelViewSet(ModelViewSet):
    serializer_class = ContainerSerializer
    queryset = Container.objects.all()


class ReagentsViewSet(APIView):
    def get(self, request):
        summary = Container.objects.values('cas', 'qualification',
                                           'name', 'formula',
                                           'density', 'location',
                                           'precursor').annotate(total_volume=Sum('volume'), total_mass=Sum('mass'))

        data = [
            {
                'name': item['name'],
                'formula': item['formula'],
                'mass': item['total_mass'],
                'volume': item['total_volume'],
                'density': item['density'],
                'location': item['location'],
                'precursor': item['precursor'],
                'cas': item['cas'],
                'qualification': item['qualification'],
            }
            for item in summary]

        return Response(data, status=status.HTTP_200_OK)
