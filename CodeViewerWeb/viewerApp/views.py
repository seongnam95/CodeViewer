from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from openpyxl import load_workbook

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


@csrf_exempt
def salary_update_excel(request):
    if request.method == 'POST':

        file = request.FILES['file_excel']
        load_wb = load_workbook(file, data_only=True)

        sheet = load_wb.active
        excel_data = pd.DataFrame(sheet.values)
        excel_data = excel_data.rename(columns=excel_data.iloc[0])
        excel_data = excel_data.drop(excel_data.index[0]).reset_index(drop=True)

        for i in excel_data.index:
            address = excel_data['도로명주소'][i].replace(' ', '')
            address = address.split('(')[0] if '(' in address else address
            excel_data['도로명주소'][i] = address

            result = processed_data(address)
            # get_old_post_num(i)

            for r in result.index:
                adr = result['도로명주소'][r].replace(' ', '')
                if adr == address:
                    excel_data['건물관리번호'][i] = result['건물관리번호'][r]

        print(excel_data)
        # 파일 저장
        # file = request.FILES['file_excel']
        # fs = FileSystemStorage()
        # filename = fs.save(file.name, file)
        # uploaded_file_url = fs.url(filename)
        # print(uploaded_file_url)

        context = {'state': True, 'rtnmsg': '{0}건의 엑셀 데이터가 반영 되었습니다.'.format(0)}
        return HttpResponse(json.dumps(context), content_type="application/json")
