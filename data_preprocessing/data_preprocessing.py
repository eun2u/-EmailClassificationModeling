import warnings
import konlpy
from konlpy.tag import *
import re
import time
def make_sentence(data):
    sentence = ""
    for i in data:
        if(i.endswith('.\n')):
            sentence+=i.replace("\n"," ")
    result = sentence.split(".")
    return result
def data_text_cleaning(data):
 
    # 특수문자 제거
    delete_spe = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\《\(\)\[\]\<\>`\'…》→㎏▶▲]', ' ', data)
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

a = input("파일명을 입력하세요(_phase2.txt 제외) : ")
f = open("./preprocessing_phase2/"+a+"_phase2.txt","r")
readdata = []
line = f.readline()
while(line):
    readdata.append(line)
    line = f.readline()
readdata = make_sentence(readdata)
print(len(readdata))
f.close()
result = []
num = 0
start = time.time()
for line in readdata:
    num+=1
    # if(num%1000==0):
    #     print(num)
    if(line!="\n"):
        data = data_text_cleaning(line)
        if(len(data)!=1):
            result.append(data)


f = open("./preprocessing_phase3/"+a+"_phase3.txt","w")
num = 0
for i in result:
    for j in i:
        f.write(j+" ")
    num+=1
    if(num%1000==0):
        print(num)
    f.write("\n")
f.close()
print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간
