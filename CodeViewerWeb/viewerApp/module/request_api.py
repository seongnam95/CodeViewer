import bs4
import requests
import pandas as pd


class RequestApi:
    def __init__(self):
        self.key = 'U01TX0FVVEgyMDIxMTIwMjEzNTc0MzExMTk4Mjc='
        self.url = 'https://www.juso.go.kr/addrlink/addrLinkApi.do'
        self.column = {'주소코드': 'admCd', '시도': 'siNm', '시군구': 'sggNm', '읍면동': 'emdNm', '법정리': 'liNm',
                       '지하여부': 'udrtYn', '번': 'lnbrMnnm', '지': 'lnbrSlno', '동': 'detBdNmList', '건물명칭': 'bdNm',
                       '도로명주소': 'roadAddrPart1', '도로명코드': 'rnMgtSn', '건물본번': 'buldMnnm', '건물부번': 'buldSlno'}
        self.column = {
            '우편번호': 'zipNo', '도로명주소': 'roadAddr', '건물명칭': 'bdNm', '건물관리번호': 'bdMgtSn'
        }

    def processed_data(self, address):
        try:
            params = {'confmKey': self.key, 'currentPage': '1', 'countPerPage': '20', 'resultType': 'xml', 'keyword': address}

            response = requests.get(self.url, params=params).text.encode('utf-8')
            xml_obj = bs4.BeautifulSoup(response, 'xml')

            rows = xml_obj.find_all('juso')

            if not rows: return None

            row_list = []
            result = pd.DataFrame(columns=list(self.column))

            column_values = list(self.column.values())
            list_append = row_list.append
            for i in range(len(rows)):
                for tag in column_values:
                    item = rows[i].find(tag)
                    if item is None:
                        list_append("")
                    else:
                        list_append(item.text.strip())
                result.loc[i] = row_list
                row_list.clear()
            return result

        except (ValueError, TypeError, IndexError) as e:
            print(f'error: {e}')
            return

        except Exception as e:
            print(f'error: {e}')
            return
