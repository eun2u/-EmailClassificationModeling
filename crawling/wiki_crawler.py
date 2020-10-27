#/Library/Frameworks/Python.framework/Versions/3.8/bin/python3
import wikipediaapi #사용할 api 호출
wiki=wikipediaapi.Wikipedia('ko') #한국 wikipedia 사이트로 접속하도록 셋팅하기

page_py = wiki.page('파이썬') 
print("Page - Exists: %s" % page_py.exists())
print("Page - Title: %s" % page_py.title)
print("Page - Summary: %s" % page_py.summary[0:100])
wiki = wikipediaapi.Wikipedia( language='ko', extract_format=wikipediaapi.ExtractFormat.WIKI) 
p_wiki = wiki.page("파이썬") 
print(p_wiki.text)

with open("파이썬.txt", "w") as f: 
    f.write(p_wiki.text)