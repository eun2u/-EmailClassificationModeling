import os
import shutil
import warnings
import konlpy
from konlpy.tag import *
import re
from gensim.models import KeyedVectors
from datetime import datetime
 
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)
def write_file(to_folder, from_folder, file):
    src = "./mail_data/"+from_folder+"/"+file
    dsc = to_folder+"/"
    shutil.copy(src,dsc)

def file_list_in_folder(folderName):
    path_dir = "./mail_data/"+folderName
    file_list = os.listdir(path_dir)
    return file_list
def testfile_list_in_folder(folderName):
    path_dir = "./test_data/"+folderName
    dir_list = os.listdir(path_dir)
    full_file_list = []
    num=0
    index_info = []
    for dir1 in dir_list:
        index_info.append([dir1.replace, num])
        path_dir = "./test_data/"+folderName+"/"+dir1
        file_list = os.listdir(path_dir)
        full_file_list.append([{i : num} for i in file_list])
        num+=1
    return index_info, full_file_list

def list_of_word_in_file(folderName, fileName):
    f = open("./mail_data/"+folderName+"/"+fileName, 'r')
    full_data = ""
    line = f.readline()
    title = line.replace("\n","")
    while(line):
        if(line != "\n"):
            if("본 메일은" in line):
                line = line.split("본 메일은")
                line = ' '.join(line[0].split())
                full_data+=line
                break
            line = line.replace("\n"," ")
            line = ' '.join(line.split())
            full_data+=line
        line = f.readline()
    f.close()
    return full_data, title

def folder_name(option1, option2, option3): #폴더명 생성
    timestr = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    full_name = "testresult_"+str(option1)+"_"+str(option2)+"_"+str(option3)+"_"+timestr
    return full_name

def findNeighborWords(loaded_model, keyword):
    flag = True
    newlist = []
    try:
        model_result=loaded_model.most_similar(keyword, topn=4)
        newlist = [[i[0],round(i[1],4)] for i in model_result if i[1] >= 0.5]
    except:
        flag = False

    return newlist, flag

def word_list(option, listData):
    wordlist = []

    if option == 2:
        loaded_model = KeyedVectors.load_word2vec_format("training_data/vector_clean_data_final_ver2_iter1000")
        for keyword in listData:
            newlist, flag = findNeighborWords(loaded_model, keyword)
            if flag:
                newlist.insert(0, [keyword, 1])
                wordlist.append(newlist)
    else:
        for keyword in listData:
            newlist = []
            newlist.append([keyword, 1])
            wordlist.append(newlist)
    return wordlist

def make_sentence(data):
    sentence = ""
    for i in data:
        if(i.endswith('.\n')):
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

    delete_list = ["이", "것", "수", "를", "개", "후", "을", "메", "의", "은", "년", "만", "그", "만", "외"]
    for i in delete_list:
        if(i in noun_data):
            noun_data.remove(i)
    return noun_data
def count_word(data):
    wordCount = {} 
    for word in data:
        # Get 명령어를 통해, Dictionary에 Key가 없으면 0리턴
        wordCount[word] = wordCount.get(word, 0) + 1   
        keys = sorted(wordCount.keys())
    count = sorted(wordCount.items(), 
                              reverse=True, 
                              key=lambda item: item[1])
    count_key = [i[0] for i in count]
    return count_key[:10]
    

def print_menu():
    print("1. 키워드 추가")
    print("2. 키워드 삭제")
    print("3. 키워드 조회")
    print("4. 키워드별 메일 확인")
    print("5. 종료")

    menu = input("메뉴 선택: ")
    return int(menu)

def splitMailHead(filename):
    mailFile = open("./mail_data/"+filename, "r")

    readdata = []
    line = mailFile.readline()
    while(line):
        readdata.append(line)
        line = mailFile.readline()
    readdata = make_sentence(readdata)
    # print(readdata)
    # print(len(readdata))
    mailFile.close()
    result = []
    num = 0
    for line in readdata:
        num+=1
        if(num%1000==0):
            print(num)
        if(line!="\n"):
            data = data_text_cleaning(line)
            if(len(data)!=1):
                result.append([line, data])
    return result


def splitKeyword():
    keywordFile = open("./visualizing_data/keyword.txt", "r")

    keywordList = keywordFile.read().split()
    
    keywordFile.close()

    return keywordList

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

def printByTitle(result, option1, option2, option3, neighborKeywords, model, score_norm):
    weightFigureList = []
    rankList = []
    for rLine in result:
        weightFigure = 0
        mailList = word_list(option3, rLine[1])
        for keywordInfo in neighborKeywords:
            word = keywordInfo[0]
            frequency = keywordInfo[1]

            if option1 == 1:
                weightFigure += findSimilarityByAvg(model, mailList, word) * frequency
            elif option1 == 2:
                weightFigure += findSimilarityBySum(model, mailList, word) * frequency
        if weightFigure >= score_norm:
            weightFigureList.append([weightFigure, rLine[0]])
            # rankList.append(["{}과 {}사이의 유사도".format(rLine[0], neighborKeywords[0][0]), weightFigure])

    sortedRankList = sorted(weightFigureList, key=lambda t: t[0], reverse=True)
    for idx in range(len(sortedRankList)):
        print("[{}]의 유사도: {}".format(sortedRankList[idx][1], sortedRankList[idx][0]))
    
    return weightFigureList


def printByContent(folderName_of_file, filelist, option1, option2, option3, neighborKeywords, model, score_norm):
    weightFigureList = []
    for filename in filelist:
        full_content , title = list_of_word_in_file(folderName_of_file, filename)
        wordlist_of_full_content = data_text_cleaning(full_content)
        weightFigure = 0
        mailList = word_list(option3, wordlist_of_full_content)
        for keywordInfo in neighborKeywords:
            word = keywordInfo[0]
            frequency = keywordInfo[1]

            if option1 == 1:
                weightFigure += findSimilarityByAvg(model, mailList, word) * frequency
            elif option1 == 2:
                weightFigure += findSimilarityBySum(model, mailList, word) * frequency
        # print("{}과 {}사이의 유사도".format(title, neighborKeywords[0][0]), weightFigure)
        if weightFigure >= score_norm:
            weightFigureList.append([weightFigure, title, filename])
    
    sortedRankList = sorted(weightFigureList, key=lambda t: t[0], reverse=True)
    for idx in range(len(sortedRankList)):
        print("[{}]의 유사도: {}".format(sortedRankList[idx][1], sortedRankList[idx][0]))

    return weightFigureList
def printByContent_freq(folderName_of_file, filelist, option1, option2, option3, neighborKeywords, model, score_norm):
    weightFigureList = []
    for filename in filelist:
        full_content , title = list_of_word_in_file(folderName_of_file, filename)
        wordlist_of_full_content = data_text_cleaning(full_content)
        wordlist_of_full_content = count_word(wordlist_of_full_content)
        weightFigure = 0
        mailList = word_list(option3, wordlist_of_full_content)
        for keywordInfo in neighborKeywords:
            word = keywordInfo[0]
            frequency = keywordInfo[1]

            if option1 == 1:
                weightFigure += findSimilarityByAvg(model, mailList, word) * frequency
            elif option1 == 2:
                weightFigure += findSimilarityBySum(model, mailList, word) * frequency
        # print("{}과 {}사이의 유사도".format(title, neighborKeywords[0][0]), weightFigure)
        if weightFigure >= score_norm:
            weightFigureList.append([weightFigure, title, filename])
    
    sortedRankList = sorted(weightFigureList, key=lambda t: t[0], reverse=True)
    for idx in range(len(sortedRankList)):
        print("[{}]의 유사도: {}".format(sortedRankList[idx][1], sortedRankList[idx][0]))

    return weightFigureList

def printResult(option1, option2, option3, wordlist, model, foldername):
    if option3 == 1 or option3 == 2:
        title_filename = input("파일 이름을 입력해주세요 : ")
        result = splitMailHead(title_filename)
        
    if option3 == 3 or option3 == 4:
        folderName_of_file = input("확인할 파일이 있는 폴더명을 입력해주세요 : ")
        filelist = file_list_in_folder(folderName_of_file)

    createFolder("./consequence/"+foldername)
    for neighborKeywords in wordlist:
        print("---------- {} 키워드 정보 ----------".format(neighborKeywords[0][0]))
        createFolder("./consequence/"+foldername+"/"+neighborKeywords[0][0])
        f = open("./consequence/"+foldername+"/"+neighborKeywords[0][0]+".txt", "w")
        # f2 = open("./consequence/"+foldername+"/not_"+neighborKeywords[0][0]+".txt", "w")
        if option3 == 1:
            if option2 == 1:
                score_norm = 0.3
            elif option2 == 2:
                score_norm = 1.0
            weightFigureList = printByTitle(result, option1, option2, option3, neighborKeywords, model, score_norm)
        elif option3 == 2:
            if option2 == 1:
                score_norm = 0.3
            elif option2 == 2:
                score_norm = 1.0
            weightFigureList = printByTitle(result, option1, option2, option3, neighborKeywords, model, score_norm)
        elif(option3 == 3):
            if option2 == 1:
                score_norm = 0.3
            elif option2 == 2:
                score_norm = 1.2
            weightFigureList = printByContent(folderName_of_file, filelist, option1, option2, option3, neighborKeywords, model, score_norm)
        elif(option3 == 4):
            weightFigureList = printByContent(folderName_of_file, filelist, option1, option2, option3, neighborKeywords, model, score_norm)

        #rankList.append(["{}과 {}사이의 유사도".format(title, neighborKeywords[0][0]), weightFigure])
        for wF in weightFigureList:
            f.write(wF[1]+"\n")
            if option3 >= 3:
                write_file("./consequence/"+foldername+"/"+neighborKeywords[0][0], folderName_of_file, wF[2])
        f.close()



def classify_mail():
    option1 = int(input("[option1] 1. avg, 2. sum : "))
    option2 = int(input("[option2] 1. user category, 2. user category+neighbor word : "))
    option3 = int(input("[option3] 1. title, 2. title+neibor word, 3. main+title, 4. main+title+freq : "))

    model = KeyedVectors.load_word2vec_format("training_data/vector_clean_data_final_ver2_iter1000")

    wordlist = word_list(option2, list(keywordSet))
    print(wordlist)
    # 함수 파라미터: option1, wordlist, model로 통일1
    foldername = folder_name(option1,option2, option3)
    printResult(option1, option2, option3, wordlist, model, foldername)


def findSimilarityBySum(model, mailData, keyword):
    sum = 0
    count = 0

    for neighborWords in mailData:
        for wordInfo in neighborWords:
            mWord = wordInfo[0]
            mFrequency = wordInfo[1]

            try:
                similarity = model.wv.similarity(mWord, keyword)
                if similarity >= 0.5:
                    similarity = 1
                sum += similarity * mFrequency
            except KeyError:
                count += 1
                continue

    return sum, count

def findSimilarityByAvg(model, mailData, word):
    sum, count = findSimilarityBySum(model, mailData, word)
    try:
        avg = sum / (len(mailData) - count)
    except ZeroDivisionError:
        avg = 0

    return avg
    
if __name__ == "__main__":
    
    keywordSet = set(splitKeyword())

    while True:
        menu = print_menu()
        if menu == 1:
            add_keyword()
            print(keywordSet)
        elif menu == 2:
            del_keyword()
        elif menu == 3:
            lookup_keyword()
        elif menu == 4:
            classify_mail()
        elif menu == 5:
            keywordFileforUpdate = open("./visualizing_data/keyword.txt", "w")
            for keyword in list(keywordSet):
                keywordFileforUpdate.write("{}\n".format(keyword))
            keywordFileforUpdate.close()
            break


