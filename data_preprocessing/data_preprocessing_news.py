import kss

a = input("문장으로 구분할 파일 이름을 입력하세요(.txt 제외) : ")
f = open("./preprocessing_phase1/"+a+".txt","r")
a = a + "_phase2"
f2 = open("./preprocessing_phase2/"+a+".txt","w")
line = f.readline()
num = 0
while(line):
    num+=1
    if(num%100==0):
        print(num)
    s = line.replace("\n","")
    for sent in kss.split_sentences(s):
        sent=sent.replace("\n","")
        if(sent.endswith(".")):  
            f2.write(sent+"\n")
        else:
            f2.write(sent+".\n")
    line = f.readline()
f.close()
f2.close()