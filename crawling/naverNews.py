# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def get_news(n_url):

    breq = requests.get(n_url)
    bsoup = BeautifulSoup(breq.content, 'html.parser')

    news_detail = bsoup.find("div", {"class": "news_end"}).text

    return news_detail


def crawler(maxpage, query, s_date, e_date):
    s_from = s_date.replace(".", "")
    e_to = e_date.replace(".", "")
    page = 1
    maxpage_t = (int(maxpage) - 1) * 10 + 1  # 11= 2페이지 21=3페이지 31=4페이지  ...81=9페이지 , 91=10페이지, 101=11페이지

    while page < maxpage_t:

        print(page)

        url = "https://search.naver.com/search.naver?where=news&query=" + query + "&sort=0&ds=" + s_date + "&de=" + e_date + "&nso=so%3Ar%2Cp%3Afrom" + s_from + "to" + e_to + "%2Ca%3A&start=" + str(
            page)

        req = requests.get(url)
        print(url)
        cont = req.content
        soup = BeautifulSoup(cont, 'html.parser')

        idx = 0
        for urls in soup.select("._sp_each_url"):
            try:
                f = open("../result/contents_text" + str(idx) + ".txt", 'w', encoding='utf-8')
                # print(urls["href"])

                news_detail = get_news(urls["href"])
                if news_detail == "":
                    continue

                for tmp in news_detail:
                    f.write(tmp)  # new style
                idx += 1
                f.close()
            except Exception as e:
                print(e)
                continue
        page += 10


def main():
    maxpage = 2
    query = "토트넘"
    s_date = "2020.01.01"
    e_date = "2020.10.27"
    crawler(maxpage, query, s_date, e_date)  # 네이버뉴스 기사내용을 크롤링

main()
