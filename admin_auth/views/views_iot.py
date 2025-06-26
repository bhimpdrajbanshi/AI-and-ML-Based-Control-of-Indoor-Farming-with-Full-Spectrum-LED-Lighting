from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from ..models import TemperatureReading

@csrf_exempt
def receive_temperature(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            temp = data.get('temperature')
            humidity = data.get('humidity')
            light = data.get('light')

            if temp is not None and humidity is not None and light is not None:
                TemperatureReading.objects.create(
                    temperature=temp,
                    humidity=humidity,
                    light=light
                )
                return JsonResponse({
                    'status': 'success',
                    'received': {
                        'temperature': temp,
                        'humidity': humidity,
                        'light': light
                    }
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Missing one or more required fields: temperature, humidity, light'
                }, status=400)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Only POST allowed'}, status=405)
