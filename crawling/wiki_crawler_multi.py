import multiprocessing
from multiprocessing import Process, Queue
import wikipediaapi #사용할 api 호출
from konlpy.tag import Okt


def work(id, queue):
    okt = Okt()
    wiki=wikipediaapi.Wikipedia('ko') #한국 wikipedia 사이트로 접속하도록 셋팅하기
    while(queue):
        vertex = queue.get()
        page_py = wiki.page(vertex) 
        if(page_py.exists()):
            print("Process %d Page - Title: %s" % (id, page_py.title))
            #print("Page - Summary: %s" % page_py.summary[0:100])
            new_words_list = okt.nouns(page_py.summary[0:100])
            for i in range(len(new_words_list)):
                queue.put(new_words_list[i])
            wiki = wikipediaapi.Wikipedia( language='ko', extract_format=wikipediaapi.ExtractFormat.WIKI) 
            p_wiki = wiki.page(vertex) 
            #print(p_wiki.text)
            with open("/Users/najihye/Desktop/4-2/종프/crawling/wiki_file/"+vertex+".txt", "w") as f: 
                f.write(p_wiki.text)
if __name__ == "__main__":
    
    thread_list = []
    queue = multiprocessing.Queue()
    item = ["광고","쇼핑","메일","고객","안내","내역","주문","정보","상품","인증","회원가입","상품","결과","발송","확인","결제","접수","공고","처리","안내","발표","이벤트","환영","통지"]
    for i in item:
        queue.put(i)
    num_cores = multiprocessing.cpu_count() # cpu core 개수
    for i in range(num_cores):
        thread_list.append(Process(target=work, args=(i+1, queue)))

    for i in thread_list:
        i.start()

    for i in thread_list:
        i.join()