import warnings
import konlpy
from konlpy.tag import *
import re
def make_sentence(data):
    print(data)
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

    delete_list = ["이", "것", "수"]
    for i in delete_list:
        if(i in noun_data):
            noun_data.remove(i)
    return noun_data


f = open("./testset/가옥.txt")
readdata = []
line = f.readline()
while(line):
    readdata.append(line)
    line = f.readline()
readdata = make_sentence(readdata)
f.close()
result = []
for line in readdata:
    print(line)
    if(line!="\n"):
        data = data_text_cleaning(line)
        if(len(data)!=1):
            result.append(data)


for i in result:
    print(i)