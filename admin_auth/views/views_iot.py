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



def temperature_data(request):
    current_read = TemperatureReading.objects.last()
    readings = TemperatureReading.objects.order_by('-timestamp')[:5]  # Last 50 readings
    data = {
        'labels': [reading.timestamp.strftime('%Y-%m-%d') for reading in readings],
        'temperature': [reading.temperature for reading in readings],
        'humidity': [reading.humidity for reading in readings],
        'light': [reading.light for reading in readings],
        'current_read': {
            'temperature': current_read.temperature,
            'humidity': current_read.humidity,
            'light': current_read.light,
            'timestamp': current_read.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        } if current_read else None,
    }
    return JsonResponse(data)


def get_data_water_tank(request):
    # latest = WaterLevel.objects.last()
    
    # if latest:
    #     return JsonResponse({
    #         'level': latest.level_cm,
    #         'time': timezone.localtime(latest.timestamp).strftime('%d %b %Y %I:%M:%S %p'),
    #         'status': "Low" if latest and latest.level_cm < 10 else "Normal" if latest and latest.level_cm < 90 else "High"

    #     })
    # else:
    return JsonResponse({
        'level': 20,
        'time': 'No data available',
        'status': 'Medium'
    })
