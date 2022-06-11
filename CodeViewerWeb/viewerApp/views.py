from django.http import JsonResponse
from django.shortcuts import render
import json

from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'index.html')


@csrf_exempt
def test(request):
    print('?')
    jsonObject = json.loads(request.body)
    print(jsonObject.get('address'))
    return JsonResponse(jsonObject)
