
f1 = open("./Newresult/insert_data_total_ver2.txt", 'r', encoding='utf-8') # -> 978006줄
f2 = open("./Newresult/clean_data_final_ver2.txt", 'w', encoding='utf-8')
cleanlist = []

# 총 몇줄인지
# print(len(f1.readlines()))

while True:
    line = f1.readline()
    if not line: break
    if line == '\n': continue
    if line not in cleanlist:
        cleanlist.append(line)
        print(len(cleanlist))
        f2.write(line)

f1.close()
f2.close()
