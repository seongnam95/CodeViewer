from django.shortcuts import render
from django.http import HttpResponse
import json

from django.views.decorators.csrf import csrf_exempt

from .module.request_api import RequestApi


# Create your views here.
def main(request):
    return render(request, 'index.html')


@csrf_exempt
def BldInfoViewer(request):
    template = 'bld_info.html'

    if request.method == 'GET':
        address = request.GET.get('address')
        request_api = RequestApi()
        result = request_api.processed_data(address)

        address_list = []
        for i in result.index:
            re_data = {'address': result['도로명주소'][i], 'num': result['건물관리번호'][i]}
            address_list.append(re_data)

        context = {'address': address_list}
        return render(request, template, context)

    return render(request, template)
# return HttpResponse(json.dumps(data), content_type='application/json')
