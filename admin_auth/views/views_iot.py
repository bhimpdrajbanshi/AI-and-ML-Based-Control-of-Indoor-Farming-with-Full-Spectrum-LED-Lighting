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

            if temp is not None:
                TemperatureReading.objects.create(temperature=temp)
                return JsonResponse({'status': 'success', 'received': temp})
            else:
                return JsonResponse({'status': 'error', 'message': 'No temperature value provided'}, status=400)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Only POST allowed'}, status=405)
