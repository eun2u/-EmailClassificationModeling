# EmailClassificationModeling

> KNU 종합설계프로젝트2 

### 1. 과제 목적 및 필요성

 지난 2018년, 만 6세 이상 인터넷 이용자의 ‘e-mail 이용률(최근 1년 이내 e-mail을 이용한 사람의 비율)’은 62.1%이다. 그 중 업무 용도로 e-mail을 이용하는 직장인 63.8%가 주 1회 이상 e-mail을 이용하고 있다. 이러한 통계 자료를 통하여 국내 e-mail 사용률이 높다는 사실을 알 수 있다. 

 이렇게 일상생활에서 매우 자주 사용하는 메신저이지만, 잦은 스팸메일과 광고성 메일로 인해 정작 중요한 정보를 놓치는 불편한 상황이 자주 발생하고 있다. 메일함을 짧은 기간이라도 방치해둔 경우, 스팸메일이 100개, 200개씩 쌓여있는 경험을 해보지 못한 사람은 없을 것이다. 그리고 그 중 대부분은 불특정 다수를 목적으로 하는 메일이기 때문에, '내가' 받을 필요가 없을 뿐더러 스팸의 내용도 나와는 관계없거나 불쾌한 내용인 경우가 상당수이다.

 따라서, 본 연구에서는 **키워드 기반 문서 범주화**를 목적으로 한다. **딥러닝을 기반으로, 키워드를 설정해 두면 그 키워드에 해당하는 문서를 추출할 수 있는 모델을 생성**할 것이다. 더 나아가 이 모델을 e-mail 서비스에 적용해 볼 것이다. 사용자가 중요한 정보를 위한 카테고리를 설정해두면 이 카테고리에 해당하는 e-mail은 자동으로 그 카테고리로 이동하게 된다. 이 기능을 통해 사용자는 수많은 메일 중에서 본인이 필요로 하는 정보만을 빠르고 편리하게 찾아볼 수 있다. 업무용 e-mail에서는 수신된 메일이 사용자가 지정한 카테고리로 정리되어 있다면 업무 효율이 더욱 증가할 것이다.



### 2. 과제 내용 및 추진 방법


사용자가 키워드를 설정할 수 있으므로, 어떠한 키워드라도 그와의 연관관계를 나타낼 수 있는 단어 벡터를 만드는 것이 우선과제이다. 따라서 e-mail뿐만 아니라, 백과사전 사이트와 뉴스들을 크롤링 하여 많은 문서들을 모으고 이를 전 처리하여 학습 가능한 데이터 셋으로 만든다. 이 데이터 셋을 기반으로 단어벡터를 모델링한다. 단어벡터가 만들어지면, 사용자가 설정해둔 키워드와 유사한 단어들을 추출한다. 새로운 메일의 제목 또는 내용에 있는 단어들과 키워드 클러스터를 비교하여 일정 유사도 이상의 결과가 나온다면, 이 메일은 사용자가 지정한 카테고리로 분류된다.


### 3. 기대효과 및 활용방안

  본 프로젝트에서 목표로 하는 키워드 기반 문서 분류 시스템을 이용하면 등록된 키워드 만으로도 수많은 양의 문서를 자동으로 분류할 수 있다. 또한 이를 프로젝트에서 핵심인 이메일 시스템에 적용했을 때의 기대효과는 다음과 같다.

--------

1. 수신한 이메일을 카테고리별로 분류함으로써 많은 광고 이메일, 또는 불필요한 이메일로 인해 놓쳤던 중요 이메일을 편하고 신속하게 확인할 수 있다.
2. 기업 내 업무용 메일 시스템에 적용한다면 메일을 다양한 기준에 따라 분류할 수 있으므로 업무 효율의 증대를 기대할 수 있다.
3. 사용자가 해당 카테고리의 메일을 수신했을 시 알람을 받고자한다면 메신저 등을 통해 알려줄 수 있도록 활용할 수 있을 것이다.

------------

 이처럼 자동 분류 이메일 시스템을 사용하면, 수많은 이메일을 수신하더라도 사용자가 분류하고자 하는 카테고리만 지정해 놓는다면 그 카테고리에 맞는 이메일을 자동으로 분류할 수 있다. 
 더 나아가, 이를 방대한 문서에서 필요한 자료를 추출하는 어떠한 시스템에라도 적용한다면 효율성과 편리성을 극대화할 수 있을 것으로 예상된다.


 ### 4. 사용 방법
 
1. mail_data 폴더 안에 분류하기 원하는 메일 데이터를 넣는다.
  + 파일 형식 : txt
  + 파일 명 : 메일 제목
  + 파일 내용 : 메일 본문
2. visualization.py을 실행한다.

 
### 5. 파일 설명
+ visualization.py : 데이터 분류 시스템
  + 사용자가 선택한 옵션으로 이메일을 분류한다.
+ training.py : 워드 임베딩 학습
+ /crawling : 데이터를 네이버 뉴스, 위키피디아, 네이버 메일, 다음 메일로부터 가져오는 파일
  + wiki_crawler.py : 위키 피디아 데이터 크롤러
  + daumNews.py : 다음 뉴스 데이터 크롤러
  + naverCrawler.py : 네이버 뉴스 데이터 크롤러
  + mail_contents_naver_crawling.py : 네이버 메일 본문 내용 크롤러
  + mail_title_naver_crawling.py : 네이버 메일 제목 크롤러
  + mail_title_daum_crawling.py : 다음 메일 제목 크롤러
+ /consequence : 분류된 결과가 저장되는 폴더
  + 분류된 시간으로된 폴더 명에 사용자가 등록해둔 키워드 폴더가 저장된다. 각 폴더 내에 분류된 이메일 파일이 저장된다.
+ /data_preprocessing : 데이터 전처리 코드가 저장된 폴더
  + data_preprocessing_news.py : 뉴스 데이터가 문장형식으로 제대로 크롤링 되지 않은 경우가 있어 이 부분을 수정한 코드
  + data_preprocessing.py : 데이터에 불용어를 제거하고, 명사만 남도록 전처리
  + data_preprocessing_multi.py : data_preprocessing.py를 멀티 프로세싱을 하여 더 빠르게 할 수 있도록 개선한 전처리 코드
+ /preprocessing_phase(n) : 데이터를 합치고, 전처리하는 단계를 총 4단계로 나눠서 했는데 이 단계별 데이터를 저장한 폴더
+ /preprocessing_final : 전처리 완료된 데이터를 저장한 폴더


 ### 6. 개선사항

1. 데이터 전처리 멀티 프로세싱으로 수정 완료
  (/data_preprocessing/data_preprocessing.py -> /data_preprocessing/data_preprocessing_multi.py)
  + 1개의 프로세스로 하던 것을 8개의 프로세스를 사용해 약 3배의 시간을 줄일 수 있었다.
2. 데이터 크롤링 멀티 프로세싱으로 수정 완료
  (/crawling/wiki_crawler.py -> /crawling/wiki_crawler_multi.py)

 