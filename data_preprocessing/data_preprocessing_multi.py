import multiprocessing
from multiprocessing import Process, Queue
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

    delete_list = ["이", "것", "수", "를", "개", "후", "을","메", "의", "은", "년", "만", "그", "만", "외", ""]
    for i in delete_list:
        if(i in noun_data):
            noun_data.remove(i)
    return noun_data
def work(id, start, end, readdata, q):
    result = []
    num = 0
    print(str(id)+" : " +str(start), str(end))
    for i in range(start, end):
        line = readdata[i]
        num+=1
        # if(i%1000==0):
        #     print("process "+str(id)+" : " + str(i))
        if(line!="\n"):
            data = data_text_cleaning(line)
            if(len(data)!=1):
                result.append(data)
    q.put(result)
    print(str(id)+" done "+str(len(result)))
    return
def getdata(id, q, result):
    while True:
        while(q.empty()): continue
        tmp = q.get()
        if tmp == 'STOP':
            break
        else:
            result.extend(tmp)
        # print(result)
            print(f"Result: {len(result)}")
    print(f"!!Result: {len(result)}")
    return
    
if __name__ == "__main__":
    a = input("파일명을 입력하세요(_phase2.txt 제외) : ")
    f = open("./preprocessing_phase2/"+a+"_phase2.txt","r")
    readdata = []
    line = f.readline()
    while(line):
        readdata.append(line)
        line = f.readline()
    readdata = make_sentence(readdata)
    END = len(readdata)
    f.close()
    print(END)
    start = time.time() 
    num = 0
    q = Queue()
    q.maxsize = END
    print(q.maxsize)
    manager = multiprocessing.Manager()

    result = manager.list()

    thread_list = []
    for i in range(6):
        thread_list.append(Process(target=work, args=(i+1, END//7*i, END//7*(i+1), readdata, q)))
    thread_list.append(Process(target=work, args=(7, END//7*6, END, readdata, q)))

    th8 = Process(target=getdata, args = (8, q, result))

    for i in thread_list:
        i.start()
    th8.start()

    for i in thread_list:
        i.join()

    q.put("STOP")
    th8.join()

    print("total size : %d"%len(result))
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
