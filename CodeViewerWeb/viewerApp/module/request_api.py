import bs4
import requests
import pandas as pd
import socket
import json

from urllib.parse import urlparse, quote


# 데이터 합치기
def matching_data(data, add_data):
    for r in data.index:
        address = data['도로명주소'].loc[r]
        for i in add_data.index:
            if address == add_data['도로명주소'].loc[i]:
                data.loc[r]['우편번호'] = add_data.loc[i]['우편번호']
    return data


# 구 우편번호
def get_old_post_num(new_address):
    full_names = {'서울': '서울특별시', '부산': '부산광역시', '대구': '대구광역시', '인천': '인천광역시', '광주': '광주광역시',
                  '대전': '대전광역시', '울산': '울산광역시', '세종': '세종시', '경기': '경기도', '강원': '강원도', '충북': '충청북도',
                  '충남': '충청남도', '전북': '전라북도', '전남': '전라남도', '경북': '경상북도', '경남': '경상남도', '제주': '제주도'}

    for i in full_names.values():
        new_address = new_address.replace(i, '')
    url = 'http://post.phpschool.com/json.phps.kr'
    params = {'addr': new_address, 'ipkey': '1740878', 'type': 'old'}
    result = json.loads(http_post(url, params))

    df = pd.DataFrame(columns=['도로명주소', '우편번호'])
    for n, i in enumerate(result['post']):
        name = i['addr_1']
        address = '%s %s %s' % (full_names[name], i['addr_2'], i['addr_3'])
        post_num = i['post']
        df.loc[n] = [address, post_num]

    return df


def catch_data(data, address):
    address = address.split('(')[0].strip().replace('  ', ' ')
    print(address)


def processed_data(address):
    try:
        key = 'U01TX0FVVEgyMDIxMTIwMjEzNTc0MzExMTk4Mjc='
        params = {'confmKey': key, 'currentPage': '1', 'countPerPage': '20', 'resultType': 'xml', 'keyword': address}
        url = 'https://www.juso.go.kr/addrlink/addrLinkApi.do'
        column = {'도로명주소': 'roadAddrPart1', '건물관리번호': 'bdMgtSn', '우편번호': ''}

        response = requests.get(url, params=params).text.encode('utf-8')
        xml_obj = bs4.BeautifulSoup(response, 'xml')
        rows = xml_obj.find_all('juso')

        if not rows: return None

        row_list = []
        result = pd.DataFrame(columns=list(column))

        column_values = list(column.values())
        list_append = row_list.append
        for i in range(len(rows)):
            for tag in column_values:
                item = rows[i].find(tag)
                if item is None: list_append("")
                else: list_append(item.text.strip())
            result.loc[i] = row_list
            row_list.clear()

        # result = matching_data(result, get_old_post_num(address))

        return result

    except (ValueError, TypeError, IndexError) as e:
        print(f'error: {e}')
        return

    except Exception as e:
        print(f'error: {e}')
        return


def http_post(url, data):
    url_info = urlparse(url)

    send_str = ''
    if data:
        for k, v in data.items():
            send_str += str(str(quote(k) + '=') + quote(v)) + '&'

    path = url_info.path
    host = url_info.hostname
    port = 80 if not url_info.port else url_info.port

    with socket.socket() as s:
        addr = (host, port)
        s.connect(addr)

        http = "POST " + str(path) + " HTTP/1.0\r\n"
        http += "Host: " + str(host) + "\r\n"
        http += "Content-Type: application/x-www-form-urlencoded\r\n"
        http += str("Content-length: " + str(len(send_str))) + "\r\n"
        http += "Connection: close\r\n\r\n"
        http += str(send_str) + "\r\n\r\n"

        s.send(http.encode())
        result = s.recv(4096)

        return result.decode('utf-8').split('\r\n\r\n')[1]
