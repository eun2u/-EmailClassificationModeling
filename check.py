from gensim.models import KeyedVectors

a = input("모델 이름 입력 : ")
loaded_model = KeyedVectors.load_word2vec_format("training_data/"+a)
while(True):
    a=input("단어를 입력해주세요 : ")
    model_result=loaded_model.most_similar(a, topn=30)
    #topn 을 정의해주면 출력 갯수를 지정할 수 있다.
    #기본값은 10
    print(model_result)
