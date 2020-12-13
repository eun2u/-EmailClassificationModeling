from gensim.models import KeyedVectors, Word2Vec
def read_insert_file():
    fread=open('./data_preprocessing/insert_data.txt','r')
    result = []
    while True:
        line = fread.readline()
        if not line: break
        line = line.replace("\n","")
        result.append(line.split(" ")[:-1])
    return result

data = read_insert_file()

model = Word2Vec(sentences=data, size=100, window=10, min_count=10, workers=4, sg=1, iter = 400)
#min_count = 5 //등장횟수가 5이하인 단어는 무시
#size = 100 //100차원 벡터 스페이스, 임베딩된 벡터의 크기
#sg = 0 // 0이면 CBOW, 1이면 skip-gram
#worker = 4 // 병렬 프로세싱 할 워커 갯수
#batch_words // 사전을 구축할 때 한번에 읽을 단어 수
model.wv.save_word2vec_format('data')


