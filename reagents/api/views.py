from django.db.models import Sum
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from reagents.serializer import ContainerSerializer
from reagents.models import Container
from authentication.api.permissions import IsAdminOrReadOnly


class ContainerModelViewSet(ModelViewSet):
    serializer_class = ContainerSerializer
    queryset = Container.objects.all()
    permission_classes = [IsAdminOrReadOnly]


class ReagentsViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        summary = Container.objects.values('cas', 'qualification', 'name',
                                           'formula', 'density', 'precursor').annotate(total_volume=Sum('volume'),
                                                                                       total_mass=Sum('mass'))
        data = [
            {
                'name': item['name'],
                'formula': item['formula'],
                'mass': item['total_mass'],
                'volume': item['total_volume'],
                'density': item['density'],
                'precursor': item['precursor'],
                'cas': item['cas'],
                'qualification': item['qualification'],
            }
            for item in summary]

        return Response(data, status=status.HTTP_200_OK)
