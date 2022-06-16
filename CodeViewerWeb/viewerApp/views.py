from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .module.request_api import *


# Create your views here.
def main(request):
    return render(request, 'index.html')


@csrf_exempt
def info_viewer(request):
    template = 'bld_info.html'
    if request.method == 'GET':
        address = request.GET.get('address')

        result = processed_data(address)
        get_old_post_num(address)

        address_list = []
        for i in result.index:
            re_data = {'zip': result['우편번호'][i], 'address': result['도로명주소'][i], 'num': result['건물관리번호'][i]}
            address_list.append(re_data)

        context = {'address': address_list}
        return render(request, template, context)

    return render(request, template)
# return HttpResponse(json.dumps(data), content_type='application/json')
