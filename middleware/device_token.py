from django.http import JsonResponse

from devices.models import Device


class DeviceTokenMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        request.device = None
        request.is_device = False

        if not request.path.startswith("/api/data/containers"):
            return self._get_response(request)

        token = request.headers.get("Device-Token")

        if not token:
            return self._get_response(request)

        try:
            device = Device.objects.get(token=token)
        except Device.DoesNotExist:
            return JsonResponse({"detail": "Invalid or inactive device token."}, status=403)

        request.device = device
        request.is_device = True
        return self._get_response(request)
