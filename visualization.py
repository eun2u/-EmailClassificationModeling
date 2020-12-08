import warnings
import konlpy
from konlpy.tag import *
import re
from gensim.models import KeyedVectors

def make_sentence(data):
    sentence = ""
    for i in data:
        if(i.endswith('다.\n')):
            sentence+=i.replace("\n"," ")
    result = sentence.split(".")
    return result

def data_text_cleaning(data):
 
    # 특수문자 제거
    delete_spe = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\《\(\)\[\]\<\>`\'…》]', ' ', data)
    # 영어 제거
    delete_eng = re.sub('[a-zA-z]',' ',delete_spe)
    #숫자 제거
    delete_num = re.sub('[0-9]',' ',delete_eng)
    #공백 한개만
    delete_blank = re.sub('\s+',' ',delete_num)
    if(delete_blank == " "):
        return " "
    # 단어만 
    warnings.simplefilter("ignore")
    mecab = Mecab()
    noun_data = mecab.nouns(delete_blank)

    delete_list = ["이", "것", "수", "를", "개", "후", "을","메", "의", "은", "년", "만", "그", "만", "외"]
    for i in delete_list:
        if(i in noun_data):
            noun_data.remove(i)
    return noun_data

def print_menu():
    print("1. 키워드 추가")
    print("2. 키워드 삭제")
    print("3. 키워드 조회")
    print("4. 키워드별 메일 확인")
    print("5. 종료")

    menu = input("메뉴 선택: ")
    return int(menu)

def splitFilebyLine(fileName):
    readdata = []
    line = fileName.readline()
    while(line):
        readdata.append(line)
        line = f.readline()
    readdata = make_sentence(readdata)
    # print(readdata)
    # print(len(readdata))
    f.close()
    return readdata

def add_keyword():
    newKeyword = input("추가할 키워드를 입력하세요: ")
    keywordSet.add(newKeyword)


def del_keyword():
    delKeyword = input("삭제할 키워드를 입력하세요: ")
    if delKeyword in list(keywordSet):
        keywordSet.remove(delKeyword)
    else:
        print("해당 키워드는 존재하지 않습니다.")


def lookup_keyword():
    print(list(keywordSet))


def classify_mail():
    model = KeyedVectors.load_word2vec_format("data")
    
    print(keywordSet)
    for keyword in list(keywordSet):
        for rLine in result:
            print("{}과 {}사이의 유사도".format(rLine, keyword))
            for rWord in rLine:
                try:
                    print(model.wv.similarity(rWord, keyword))
                except KeyError:
                    continue

if __name__ == "__main__":
    f = open("/Users/user/Downloads/dayoon98_naver.txt")
    
    readdata = splitFilebyLine(f)
    result = []
    num = 0
    for line in readdata:
        num+=1
        if(num%1000==0):
            print(num)
        if(line!="\n"):
            data = data_text_cleaning(line)
            if(len(data)!=1):
                result.append(data)
    
    # print(result)

    keyword_File = open("/Users/user/Downloads/keyword.txt", "a+")
    keywordSet = set(splitFilebyLine(keyword_File))

    while True:
        menu = print_menu()
        if menu == 1:
            add_keyword()
        elif menu == 2:
            del_keyword()
        elif menu == 3:
            lookup_keyword()
        elif menu == 4:
            classify_mail()
        elif menu == 5:
            break


