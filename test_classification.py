import os
def testfile_list_in_folder(folderName):
    path_dir = "./test_data/"+folderName
    dir_list = os.listdir(path_dir)
    full_file_list = {}
    num=0
    index_info = {}
    for dir1 in dir_list:
        
        index_info[dir1] = num
        path_dir = "./test_data/"+folderName+"/"+dir1
        file_list = os.listdir(path_dir)
        for i in file_list:
            full_file_list[i] = num
        num+=1
    return index_info, full_file_list
def checkfile_list_in_folder(folderName, index_info, testfolderName):
    path_dir = "./consequence/"+folderName
    path_dir2 = "./mail_data/"+testfolderName
    dir_list = os.listdir(path_dir)
    dir_list2 = os.listdir(path_dir2)
    full_file_list = {}
    for dir1 in dir_list:
        if not dir1.endswith(".txt"):
            num = index_info[dir1]
            path_dir = "./consequence/"+folderName+"/"+dir1
            file_list = os.listdir(path_dir)
            for i in file_list:
                full_file_list[i] = num
    print(len(full_file_list))
    for i in dir_list2:
        if i not in full_file_list.keys():
            full_file_list[i] = 1
    return full_file_list
def check(list1, list2):
    total_num = 100
    num=0
    print(len(list2))
    for i in list2.keys():
        if(list1[i] == list2[i]):
            num+=1
    print(str(num/total_num*100)+"%")
        
if __name__ == "__main__":

    index_info, full_file_list = testfile_list_in_folder("test2") #인덱스 정보 받아오기
    # print(full_file_list)
    testfoldername = input("테스트한 데이터가 있는 폴더 : ")
    foldername = input("결과를 비교할 폴더 이름 : ")
    full_file_list2 = checkfile_list_in_folder(foldername, index_info, testfoldername)
    print(index_info)
    print(full_file_list2)
    check(full_file_list, full_file_list2)


