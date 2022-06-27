import bs4
import requests
import pandas as pd
import pymysql


def dbcon():
    host = 'db.snserver.site'
    conn = pymysql.connect(
        host=host, user='jsn0509', password='ks05090818@', db='dbjsn0509', charset='utf8')
    return conn


def get_old_post_num(params):
    return


# 데이터 합치기
def matching_data(data, add_data):
    for r in data.index:
        address = data['도로명주소'].loc[r]
        for i in add_data.index:
            if address == add_data['도로명주소'].loc[i]:
                data.loc[r]['우편번호'] = add_data.loc[i]['우편번호']
    return data


# 구 우편번호
def get_old_post_num2(new_address):
    full_names = {'서울': '서울특별시', '부산': '부산광역시', '대구': '대구광역시', '인천': '인천광역시', '광주': '광주광역시',
                  '대전': '대전광역시', '울산': '울산광역시', '세종': '세종시', '경기': '경기도', '강원': '강원도', '충북': '충청북도',
                  '충남': '충청남도', '전북': '전라북도', '전남': '전라남도', '경북': '경상북도', '경남': '경상남도', '제주': '제주도'}

    for i in full_names.values():
        new_address = new_address.replace(i, '')
    # 애니웨어: 3092219 # 가비아 1740878
    url = 'http://post.phpschool.com/json.phps.kr'

    params = {'addr': new_address, 'ipkey': '3092219', 'type': 'old'}

    response = requests.post(url, data=params, verify=False)
    print('## response ########## :', response)
    result = response.json()

    df = pd.DataFrame(columns=['도로명주소', '우편번호'])
    print(result)

    if 'post' in result.keys():
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
        column = {'도로명주소': 'roadAddrPart1', '도로명코드': 'rnMgtSn', '건물번호본번': 'buldMnnm', '건물번호부번': 'buldSlno',
                  '건물관리번호': 'bdMgtSn', '우편번호': ''}

        response = requests.post(url, params=params, verify=False).text.encode('utf-8')
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

        print(result)

        db = dbcon()
        c = db.cursor()

        for i in result.index:
            row = result.loc[i]
            code, bld_bon, bld_bu = row['도로명코드'], row['건물번호본번'], row['건물번호부번']

            where = f"""`도로명코드`='{code}' AND `건물번호본번`='{bld_bon}' AND `건물번호부번`='{bld_bu}'"""
            print(where)
            c.execute(f"SELECT `우편번호` FROM `post_num_db` WHERE {where}")

            post_num = c.fetchall()[0]
            result['우편번호'] = post_num[0]

        db.commit()
        db.close()

        return result

    except (ValueError, TypeError, IndexError) as e:
        print(f'error: {e}')
        return

    except Exception as e:
        print(f'error: {e}')
        return
