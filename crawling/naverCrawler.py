import urllib
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests
import urllib.request
from yarl import URL
import trafilatura

all_url = []
index = 0
trash = ['Å', '¼', 'ö', '¼', 'À', '¯', 'Ô', '¡', 'Ä', 'Ú', '½', 'º', 'Ç','Ç', '»', 'ó', 'Â', 'Ã', 'â', 'ß']

def issame(url, query):
    # 중복검사
    #print("In issame")
    count = 0
    if url in all_url:
        count += 1
    if count == 0:
        store(url, query)

def store(url, query):
    global all_url
    global index
    all_url.append(url)

    try:
        downloaded = trafilatura.fetch_url(url)
        result = trafilatura.extract(downloaded)
        if bool(result) and not any(t in trash for t in result):
            f = open("./result/" + query + "_" + str(index) + ".txt", 'w', encoding='utf-8')
            f.write(result)
            f.close()
            index += 1
            print(result)

    except Exception as e:
        print(e)

def allList(url, query):
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    print("in allList")

    try: # requests.get(url, verity=false)로 response 확인 필요함
        r = requests.get(url, verify=False)

        # 첫 인자는 html소스코드, 두 번째 인자는 어떤 parser를 이용할지 명시
        soup = BeautifulSoup(r.text, "html.parser")

        # 전체 html에서 body의 a태그 모두 찾기
        a_tags = soup.find('body').findAll("a")

        # 모든 a태그를 돌면서 링크가 존재하는 href속성 추출하기
        for a_tag in a_tags:
            if "href" in str(a_tag):  # a태그 안에 href속성이 존재하는지 확인
                    #print(a_tag)
                if a_tag["href"].startswith("http"):  # 정상적인 url형식인지 확인
                    ch_url = a_tag["href"]
                    if "news" in ch_url :
                        if "news.naver.com" not in ch_url and "nid" not in ch_url and "help.naver.com" not in ch_url:
                                #print(ch_url)
                            issame(ch_url, query)

            else:
                continue
    except:
        pass


s_date = "2010.01.01"
e_date = "2018.04.20"
s_from = s_date.replace(".", "")
e_to = e_date.replace(".", "")
queryList = ["광고", "쇼핑", "상품", "취업", "대학교"]

for query in queryList:
    index = 0
    page = 1
    while page < 100:
        print(page)
        url = "https://search.naver.com/search.naver?where=news&query=" + query + "&sort=1&ds=" + s_date + "&de=" + e_date + "&nso=so%3Ar%2Cp%3Afrom" + s_from + "to" + e_to + "%2Ca%3A&start=" + str(page)
        print(url)
        allList(url, query)
        page += 10





