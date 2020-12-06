from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import random
import time
from bs4 import BeautifulSoup
import pyperclip 
from secret import NAVER

def move_to_mailbox():
    driver.find_element_by_xpath('//*[@id="0_fol"]/span/a[1]').click()
    #time.sleep(3)

def get_mail_list():

    html=driver.page_source
    soup=BeautifulSoup(html,'html.parser')
    pages=soup.select('span.pageSelector')
    lastpage=pages[0].attrs["lastpage"]
    fileOut = open('/Users/han-eunju/Desktop/mailCrawl/'+ myId+ '_naver.txt', 'w', encoding='utf-8')

    for i in range(2,int(lastpage)+1):            
        div_list = soup.select("ol.mailList > li > div.mTitle")
        for div in div_list:
            soup = BeautifulSoup(str(div), "html.parser")
            title = soup.select_one("div.name > a").text
            subject = soup.select_one("div.subject > a:nth-of-type(1) > span > strong").text
            #print("{} / {}".format(title, subject),file=fileOut)    
            print(subject[6:],file=fileOut)

        if(i%10==1):
            path='//*[@id="next_page"]'
        else: 
            path='//*[@id="'+ str(i) +'"]'
        
        driver.find_element_by_xpath(path).click()
        #time.sleep(2) 
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

move_to_mailbox()
get_mail_list()
prevent_close()
