import bs4
import requests
import pandas as pd
import pymysql


def dbcon():
    host = 'db.snserver.site'
    conn = pymysql.connect(
        host=host, user='jsn0509', password='ks05090818@', db='dbjsn0509', charset='utf8')
    return conn


def processed_data(address):
    try:
        key = 'U01TX0FVVEgyMDIxMTIwMjEzNTc0MzExMTk4Mjc='
        params = {'confmKey': key, 'currentPage': '1', 'countPerPage': '20', 'resultType': 'xml', 'keyword': address}
        url = 'https://www.juso.go.kr/addrlink/addrLinkApi.do'
        column = {'도로명주소': 'roadAddrPart1', '도로명코드': 'rnMgtSn', '건물번호본번': 'buldMnnm', '건물번호부번': 'buldSlno',
                  '도로명': 'rn', '건물관리번호': 'bdMgtSn', '우편번호': 'zipNo', '구우편번호': ''}

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

        db = dbcon()
        c = db.cursor()

        where = []
        for i in result.index:
            row = result.loc[i]
            road, bld_bon, bld_bu = row['도로명'], row['건물번호본번'], row['건물번호부번']
            where.append(f"""`도로명`='{road}' AND `건물번호본번`='{bld_bon}' AND `건물번호부번`='{bld_bu}'""")

        c.execute(f"SELECT `우편번호`, `도로명코드`, `건물번호본번`, `건물번호부번` FROM `post_num_db` WHERE {' OR '.join(where)}")

        for i, r in enumerate(c.fetchall()):
            row = result[(result['도로명코드'] == r[1]) & (result['건물번호본번'] == r[2]) & (result['건물번호부번'] == r[3])].index
            result['구우편번호'].loc[row] = r[0]

        for i in result.index:
            if len(result['구우편번호'].loc[i]) == 0:
                result['구우편번호'].loc[i] = result['우편번호'].loc[i]
        print(result)
        db.commit()
        db.close()

        return result

    except (ValueError, TypeError, IndexError) as e:
        print(f'error: {e}')
        return

    except Exception as e:
        print(f'error: {e}')
        return
