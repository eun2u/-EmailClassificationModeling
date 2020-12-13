from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import random
import time
from bs4 import BeautifulSoup
import pyperclip 
from secret import NAVER

cnts=0

def move_to_mailbox():
    driver.find_element_by_xpath('//*[@id="0_fol"]/span/a[1]').click()
    #time.sleep(3)

def crawl_contents(num, title):
    global cnts
    cnts+=1

    print(title[6:])
    fileOut = open('/Users/han-eunju/Desktop/mailCrawl/naver_'+ myId+ '/'+str(cnts)+'.txt', 'w', encoding='utf-8')
    #fileOut = open('/Users/han-eunju/Desktop/mailCrawl/naver_'+ myId+ '/'+ title[6:] +'.txt', 'w', encoding='utf-8')
    
    print(title[6:]+'\n',file=fileOut)
    
    time.sleep(0.5)
    mailPath='//*[@id="list_for_view"]/ol/li[' + str(num)+ ']/div/div[2]'
    element = driver.find_element_by_xpath(mailPath)
    driver.execute_script("arguments[0].click();", element)
    time.sleep(0.5)

    #내용 크롤링
    html=driver.page_source
    soup=BeautifulSoup(html,'html.parser')
    time.sleep(0.5)
    contents = soup.select_one("div.coverWrap > div#readFrame")
    
    if contents is None:
        driver.back()
    else:
        print(contents.text,file=fileOut)
        #contents=contents.text.strip()
        driver.back()
    
    time.sleep(0.5)


def get_maillist_and_click():
    html=driver.page_source
    soup=BeautifulSoup(html,'html.parser')
    pages=soup.select('span.pageSelector')
    lastpage=pages[0].attrs["lastpage"]

    for i in range(2,int(lastpage)+1):    
                
        div_list = soup.select("ol.mailList > li > div.mTitle")
        for div_num in range(len(div_list)):
            soup = BeautifulSoup(str(div_list[div_num]), "html.parser")
            sender = soup.select_one("div.name > a").text
            title = soup.select_one("div.subject > a:nth-of-type(1) > span > strong").text
            
            #발신자 'Facebook'인 경우 출력안함
            if 'Facebook' in sender:
                continue
            
            #메일 클릭해서 내용보기
            crawl_contents(div_num+1,title)
        
        if(i%10==1): #마지막이면 다음버튼을 클릭
            path='//*[@id="next_page"]'
        else: #마지막이 아니면 숫자페이지 클릭
            path='//*[@id="'+ str(i) +'"]'
        
        #다음 페이지 클릭
        driver.find_element_by_xpath(path).click()
        time.sleep(0.5) 
        html=driver.page_source
        soup=BeautifulSoup(html,'html.parser')


def prevent_close():
    user_choice=input('Press [ENTER] to terminate')
    if not user_choice:
        print("terminated...")
        quit()

def clipboard_input(user_xpath, user_input):
        temp_user_input = pyperclip.paste()  # 사용자 클립보드를 따로 저장

        pyperclip.copy(user_input)
        driver.find_element_by_xpath(user_xpath).click()
        ActionChains(driver).key_down(Keys.COMMAND).send_keys('v').key_up(Keys.CONTROL).perform()

        pyperclip.copy(temp_user_input)  # 사용자 클립보드에 저장된 내용을 다시 가져옴
        time.sleep(1)


# 맥은 chrome Driver안되는 경우 발생해서 firefox 사용
#driver = webdriver.Firefox(capabilities=None, executable_path='/usr/local/bin/geckodriver')
driver=webdriver.Chrome('/Users/han-eunju/Downloads/chromedriver')

driver.get("https://nid.naver.com/nidlogin.login")

myId=NAVER["id"]
myPass=NAVER["password"]

clipboard_input('//*[@id="id"]', myId)
clipboard_input('//*[@id="pw"]', myPass)
driver.find_element_by_xpath('//*[@id="log.login"]').click()


driver.get('https://mail.naver.com/')

#move_to_mailbox()
get_maillist_and_click()
prevent_close()
