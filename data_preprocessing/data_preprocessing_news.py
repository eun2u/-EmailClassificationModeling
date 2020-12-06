import kss

f = open("./NaverCrawlingTotal.txt","r")
f2 = open("./file.txt","w")
line = f.readline()
num = 0
while(line):
    num+=1
    if(num%100000==0):
        print(num)
    s = line.replace("\n","")
    for sent in kss.split_sentences(s):
        sent=sent.replace("\n","")
        if(sent.endswith(".")):  
            print("if")
            f2.write(sent+"\n")
        else:
            print("else")
            f2.write(sent+".\n")
    line = f.readline()
f.close()
f2.close()