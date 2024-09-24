from pydoc import resolve

from django.http import JsonResponse
from devices.models import Device

class DeviceTokenMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        print(request.path)
        if not request.path.startswith("/data/containers"):
            return self._get_response(request)

        token = request.headers.get("Device-Token")

        if not token:
            return self._get_response(request)

        try:
            device = Device.objects.get(token=token)
        except Device.DoesNotExist:
            return JsonResponse({'detail': 'Invalid or inactive device token.'}, status=403)

        request.device = device
        return self._get_response(request)