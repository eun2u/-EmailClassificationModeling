import secret
from bs4 import BeautifulSoup
from selenium import webdriver

# chromedriver 설정
driver = webdriver.Chrome('/Users/han-eunju/Downloads/chromedriver')
driver.implicitly_wait(3)

# 네이버 로그인 페이지로 이동
driver.get('https://nid.naver.com/nidlogin.login')

# id와 password 정보 가져오기
idwd = secret.ID
pswd = secret.PSWD

# id와 password 입력
driver.find_element_by_name('id').send_keys(idwd)
driver.find_element_by_name('pw').send_keys(pswd)

# 로그인 버튼 클릭
driver.find_element_by_class_name('btn_global').click()
# 자주 사용하는 브라우저 등록 해제
driver.find_element_by_class_name('btn_cancel').click()

# 네이버 메일로 이동
driver.get('https://mail.naver.com')

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# 보낸사람을 가져온다
sendlist = soup.find_all('div', 'name _ccr(lst.from) ')

# class가 blind인 span을 제거한다
[s.extract() for s in soup('span', {'class':'blind'})]
# 메일 제목을 가져온다
titlelist = soup.find_all('div', 'subject')

# 모두 출력한다
for i in range(len(sendlist)):
    print(sendlist[i].find('a').get_text())
    print(titlelist[i].find('strong').get_text())
    print()
