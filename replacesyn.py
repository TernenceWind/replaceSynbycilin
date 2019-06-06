# coding = utf-8
import numpy as np
import os
from pyltp import Segmentor
import random

DIR = 'ltp_data_v3.4.0'
cws_model_path = os.path.join(DIR, 'cws.model')
seg = Segmentor()
seg.load(cws_model_path)

# 构建同义词表
cilinpath = 'cilin.txt'
synwords = []
with open(cilinpath,'r',encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        temp = line.strip()
        split = temp.split(' ')
        bianhao = split[0]
        templist = split[1:]
        if bianhao[-1] == '=':
            synwords.append(templist)
print(len(synwords))
print(synwords[100])

files = ['1电子-digit_all.txt','-1电子-digit_all.txt','0电子-digit_all.txt']
lengths = [50,20,10]
kvalues = [1,3,3]

for line in range(len(files)):
    faddpath = '_add_'+files[line]
    faddinstances = []
    flag = True
    while flag:
        processfile(files[line],lengths[line],kvalues[line])
        addtemp = readfile('add_'+files[line])
        datatemp = readfile(files[line])
        faddinstances += addtemp
        datatemp += addtemp
        datatemp = list(set(datatemp))
        writefile(files[line],datatemp)
        if len(datatemp) >= lengths[line]:
            flag = False
    faddinstances = list(set(faddinstances))
    writefile(faddpath,faddinstances)



# 查词函数
def findsyn(word):
    if len(word) == 1:
        return []
    tempsynwords = synwords[:]
    np.random.shuffle(tempsynwords)
    for line in tempsynwords:
        if word in line:
            templine = line[:]
            for i in line:
                if len(i) == 1:
                    templine.remove(i)
            return templine
    return []

#  切分极性
def cutPolarities(path):
    neutral = []
    positive = []
    negative = []
    file = open(path, 'r', encoding='utf-8')
    lines = file.readlines()
    for line in lines:
        temp = line.strip().split('<ssssss>')
        if len(temp) != 3:
            print(line)
        if ',1)'in temp[2]:
            positive.append(line.replace(' ',''))
        if ',-1)' in temp[2]:
            negative.append(line.replace(' ',''))
        if ',0)' in temp[2]:
            neutral.append(line.replace(' ',''))
    file.close()
    print("正向%d条，负向%d条，中性%d条" %(len(positive),len(negative),len(neutral)))
    # 存入文件
    pfile = open('1'+path, 'w', encoding='utf-8')
    pfile.write(''.join(positive))
    pfile.close()
    neufile = open('0'+path, 'w', encoding='utf-8')
    neufile.write(''.join(neutral))
    neufile.close()
    nagfile = open('-1'+path, 'w', encoding='utf-8')
    nagfile.write(''.join(negative))
    nagfile.close()

# 读写文件
def readfile(path):
    result = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            result.append(line.strip())
    return result
def writefile(path, result):
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(result))   

# 处理文本进行单句替换
def processfile(path, maxlen, kvalue):
    file = readfile(path)
    file = list(set(file))
    add = []
    i = 0
    while len(add)+len(file) < maxlen:
        np.random.shuffle(file)
        temp = replacesyn(file[0], kvalue)
        if temp == "":
            continue
        for i in temp:
            add.append(i)
        add = list(set(add))
    print(len(file),len(add))
    writefile('add_'+path, add)
    writefile(path,file)

# 替换同义词，返回替换好的若干句完整的话
def replacesyn(sent, kvalue):
    split = sent.split('<ssssss>')
    question = seg.segment(split[0])
    answer = seg.segment(split[1])
    # 首先确认问答中各有几个词被替换
    if len(question) < 2:
        qlen = 1
    else:
        qlen = int(len(question)//2)
    if len(answer) < 2:
        alen = 1
    else:
        alen = int(len(answer)//2)
    # 确定被替换词的编号
    qlist = random.sample(range(0,len(question)),qlen)
    alist = random.sample(range(0,len(answer)),alen)
    
    # 被抽中的词列表
    changewords = []
    for i in qlist:
        if question[i] not in changewords:
            changewords.append(question[i])
    for i in alist:
        if answer[i] not in changewords:
            changewords.append(answer[i])
    
    # question
    qs = []
    for k in range(kvalue):
        tempq = question[:]
        for i in qlist:
            #print(i,question[i])
            nearby = findsyn(question[i])
            if len(nearby) > 0:
                temprandom = random.sample(range(0,len(nearby)),1)[0]
                tempq[i] = nearby[temprandom]
        qs.append(''.join(tempq))
                  
    # answer
    ans = []
    for k in range(kvalue):
        tempa = answer[:]
        for i in alist:
            nearby = findsyn(answer[i])
            if len(nearby) > 0:
                temprandom = random.sample(range(0,len(nearby)),1)[0]
                tempa[i] = nearby[temprandom]
        ans.append(''.join(tempa))

    # labeltuple
    labelstrs = split[2].split(')')[:-1]
    ls = []
    for k in range(kvalue):
        templabel = labelstrs[:]
        for i in range(len(labelstrs)):
            strlist = labelstrs[i].split(',')
            temp = strlist[0][1:]
            if (temp not in qs[k]) and (temp not in ans[k]):
                if temp not in changewords:
                    return ""
                else:
                    nearby = findsyn(temp)
                    for one in nearby:
                        if one in qs[k] or one in ans[k]:
                            strlist[0] = '(' + one
            templabel[i] = ','.join(strlist)
        ls.append(')'.join(templabel)+')')
    
    result = []
    for k in range(kvalue):
        temp = qs[k]+'<ssssss>'+ans[k]+'<ssssss>'+ls[k]
        result.append(temp)
        
    return result