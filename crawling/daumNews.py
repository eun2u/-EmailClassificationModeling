from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup
kindlist = ['digital/it' ,'digital/device']
#'society', , 'economic', 'foreign', 'culture','entertain','sports','digital'
for kind in kindlist:
    #print(kind)
    for page in range(1, 2):
        # print(page)
        res = requests.get(f'https://news.daum.net/breakingnews/{kind}?page={page}')
        if '해당 일자에 데이터가 없습니다.' in res.text:
            print(res.text.find('해당 일자에 데이터가 없습니다.'))
            break
        soup = BeautifulSoup(res.content, 'html.parser')
        link = soup.select(' .tit_thumb > a')
        for a in link:
            # print(a.attrs["href"])
            adr = a.attrs["href"]
            # print(f'{a.attrs["href"]}| {a.text}\n' )
            html = requests.get(adr)
            bsObject = BeautifulSoup(html.content, "html.parser")
            with open(f'../crawling/{adr[-5:]}.txt', 'w', encoding='UTF8') as f:
                for link in bsObject.find_all('p'):
                    str = link.text.strip()
                    f.write(str)
                f.write('\n')
                f.close()