from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from openpyxl import load_workbook

from .module.request_api import *


def main(request):
    return render(request, 'index.html')


@csrf_exempt
def info_viewer(request):
    template = 'bld_info.html'
    if request.method == 'GET':
        address = request.GET.get('address')
        result = processed_data(address)

        if result is not None:

            address_list = []
            for i in result.index:
                re_data = {'zip': result['구우편번호'][i], 'old': result['주소'][i], 
                           'address': result['도로명주소'][i], 'num': result['건물관리번호'][i]}
                address_list.append(re_data)

            context = {'address': address_list}
            return render(request, template, context)

    return render(request, template)
# return HttpResponse(json.dumps(data), content_type='application/json')
