from selenium import webdriver
from selenium.webdriver import Chrome
import time
from bs4 import BeautifulSoup
from secret import DAUM

def login_to_kakao():
    #다음, 카카오 중 카카오로 로그인
    login_url = 'https://accounts.kakao.com/login?continue=https%3A%2F%2Flogins.daum.net%2Faccounts%2Fksso.do%3Frescue%3Dtrue%26url%3Dhttps%253A%252F%252Fwww.daum.net%252F'
    driver.get(login_url)
    
    id_input = driver.find_element_by_name('email')
    id_input.send_keys(myId)

    pwd_input = driver.find_element_by_name('password')    
    pwd_input.send_keys(myPass)

    driver.find_element_by_xpath('//*[@id="login-form"]/fieldset/div[8]/button[1]').click()
    time.sleep(1)

def login_to_daum():
    #다음, 카카오 중 다음으로 로그인
    login_url='https://logins.daum.net/accounts/signinform.do?url=https%3A%2F%2Fwww.daum.net%2F'
    driver.get(login_url)

    id_input = driver.find_element_by_name('id')
    id_input.send_keys(myId)

    pwd_input = driver.find_element_by_name('pw')
    pwd_input.send_keys(myPass)

    driver.find_element_by_xpath('//*[@id="login-form"]/fieldset/div[8]/button[1]').click()
    time.sleep(1)

 
def move_to_mailbox():
    mail_url = 'https://mail.daum.net/'
    driver.get(mail_url)
    time.sleep(1)

def print_mails(link_list,fileOut):
    for a in link_list:
        link = a.get_attribute('href')
        title = a.text.strip()
        print(title,file=fileOut)


def get_mail_list():
    fileOut = open('/Users/han-eunju/Desktop/mailCrawl/daum_'+ myId+ '.txt', 'w', encoding='utf-8')

    html=driver.page_source
    soup=BeautifulSoup(html,'html.parser')
    pages=soup.select('.link_page')
    length=len(pages)
    print(length)

    while(True):
        link_list = driver.find_elements_by_css_selector('div#mailList a.link_subject')
        
        if(length==1):
            print_mails(link_list,fileOut)
            break
        else:
            for i in range(2,length+1):
                print_mails(link_list,fileOut)
                
                nextPath='//*[@id="mailList"]/div[1]/div/div[3]/div/span/a['+str(i)+']'
                driver.find_element_by_xpath(nextPath).click()
                time.sleep(0.3)
                link_list = driver.find_elements_by_css_selector('div#mailList a.link_subject')
            
            print_mails(link_list,fileOut)
            if(length==10): 
                nextPath='//*[@id="mailList"]/div[1]/div/div[3]/div/span/a[11]' 
                driver.find_element_by_xpath(nextPath).click()
                time.sleep(0.3)
            else:
                break

        html=driver.page_source
        soup=BeautifulSoup(html,'html.parser')
        pages=soup.select('.link_page')
        length=len(pages)
        print(length)

def prevent_close():
    user_choice=input('Press [ENTER] to terminate')
    if not user_choice:
        print("terminated...")
        quit()


myId=DAUM["id"]
myPass=DAUM["password"]

driver=webdriver.Chrome('/Users/han-eunju/Downloads/chromedriver')
login_to_kakao
#login_to_daum()
move_to_mailbox()
get_mail_list()
prevent_close()