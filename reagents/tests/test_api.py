from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_200_OK, HTTP_201_CREATED

from reagents.models import Container


class ReagentsApiTestCase(APITestCase):
    def test_data(self):
        Container.objects.create(container_id=1, name="aba", formula="aba", mass=12, volume=23, density=20,
                                      location="dad", precursor=True, cas="ab23b", qualification=20)
        Container.objects.create(container_id=2, name="aba", formula="aba", mass=242, volume=190, density=20,
                                      location="dad", precursor=True, cas="ab23b", qualification=20)

        url = reverse('data:containers-list')
        print(url)
        #response = self.client.get(url)
        #print(response.data)
