from rest_framework.serializers import ModelSerializer

from reagents.models import Container


class ContainerSerializer(ModelSerializer):
    class Meta:
        model = Container
        fields = "__all__"
