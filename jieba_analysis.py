import readfiles as RF
import jieba
import pandas as pd
import numpy as np
from  textblob import TextBlob
import jieba.analyse

## add new target words_list ##
jieba.load_userdict("add_vocabulary/fixed_vocabulary.txt")
jieba.load_userdict("add_vocabulary/date_collection.txt")

## 趋势词分类相对路径 ##
trend_directory0='classify/negative_word.txt'
trend_directory1='classify/neutral_word.txt'
trend_directory2='classify/positive_word.txt'


## 过滤函数 ： 过滤掉初步分词后的 无实际意义的词 ##
def jiebaclearText(content,stopwords_directory):
    clearedwords=[]
    seg_list = jieba.cut(content,cut_all=False)
    liststr="/".join(seg_list)
    f_stop_text=RF.content(stopwords_directory)
    f_stop_seg_list=f_stop_text.split("\n")
    for word in liststr.split("/"):
        if not(word.strip()) in f_stop_seg_list and len(word.strip()) > 1:
            clearedwords.append(word)
    return '/'.join(clearedwords)

## 过滤为趋势词汇函数 ##
def jiebaclearVocabularies(Vocabularies):
    clearedwords=[]
    f_trend_text=RF.content(trend_directory)
    f_trend_seg_list=f_trend_text.split("\n")
    for word in Vocabularies.split("/"):
        if (word.strip()) in f_trend_seg_list and len(word.strip()) > 1:
            clearedwords.append(word)
    if len(clearedwords)==0:
        return 'non_content'
    else:
        return '/'.join(clearedwords)

## 过滤为趋势词汇函数并进行分类 ##
def jiebaclearVocabulariesandClassify(Vocabularies):
    clearedwords = []
    f_classify0_text = RF.content(trend_directory0)
    f_classify1_text = RF.content(trend_directory1)
    f_classify2_text = RF.content(trend_directory2)
    f_classify0_list = f_classify0_text.split("\n")
    f_classify1_list = f_classify1_text.split("\n")
    f_classify2_list = f_classify2_text.split("\n")

    for word in Vocabularies.split("/"):
        if (word.strip()) in f_classify0_list and len(word.strip()) > 1:
            clearedwords.append((word,-1))
        elif (word.strip()) in f_classify1_list and len(word.strip()) > 1:
            clearedwords.append((word, 0))
        elif (word.strip()) in f_classify2_list and len(word.strip()) > 1:
            clearedwords.append((word, 1))
    return clearedwords

## 单词重建 ：构建新的合成词 ##
def restructureword(content,num):
    newcontent=[]
    words=content.split("/")
    wordsnum=len(words)
    for i in range(wordsnum):
        if i <= wordsnum-num:
            newword=""
            for i in range(i,i+num):
                newword+=words[i]
            newcontent.append(newword)
        else:
            break
    return newcontent


def Indexs(content, word):
    indexs=[]
    if len(content) == 0 or len(word) == 0 or len(content) < len(word):
        return indexs
    else:
        count = 0
        index = 0
        while True:
            answer=content.find(word)
            if answer != -1:
                content = content[answer + 1:]
                count += 1
            else:
                break
            if count == 1:
                index = index + answer
            else:
                index = index + answer + 1
            indexs.append(index)
        return indexs


## 输出一篇文章的单词，过滤频率 小于等于 1 的复合单词，同时输出相应的偏移量 ##
def TopN(content,recontent,Counts):
    resultlist=[]
    dict1 = {}
    dict2 = {}
    for word in recontent:
        indexs =Indexs(content, word)
        length=len(indexs)

        ## delete出现次数小于等于 1 的重构词 ##
        #if length!=0
        if length>=Counts:
            dict1[word] = indexs
            dict2[word] = length
    newdict2 = sorted(dict2.items(), key=lambda x: x[1], reverse=True)
    keywords = list(map(lambda x:x[0],newdict2))
    for keyword in keywords:
        resultlist.append((keyword,dict2[keyword],dict1[keyword]))
    return resultlist


## 提取相应合成词在 文章中的 对应的整个句子 ##
def Sentences(filenum,content,result,out_name):
    a = Indexs(content, "。")
    b = content.split("。")
    #添加最后一行
    x=a[len(a)-1]
    y=len(b[len(b)-1])
    a.append(x+y)
    c=zip(a,b)
    c=list(c)
    datas=[]
    for name,number,indexs in result:
        data=[]
        data.append(name)
        data.append(number)

        for index in indexs:
            for j in range(len(c)):
                if index < c[j][0] or index == c[j][0]:
                    data.append(c[j][1])
                    break
        datas.append(data)
    max_len = len(datas[0])
    for i_add in range(len(datas)):
        repeat_part = ['non_content'] * (max_len - len(datas[i_add]))
        datas[i_add].extend(repeat_part)
    out_file = pd.DataFrame(np.array(datas))
    out_file.to_csv('jieba_result/'+out_name + str(filenum) + '.csv')

## 文章进行段落偏移并输出对应从*****关键字*****开始的整个句子 ##
def NewSentences(filenum,content,result,out_name):
    a = Indexs(content, "。")
    b = content.split("。")
    #添加最后一行
    x=a[len(a)-1]
    y=len(b[len(b)-1])
    a.append(x+y)
    c=zip(a,b)
    c=list(c)
    datas=[]
    for name,number,indexs in result:
        data=[]
        data.append(name)
        data.append(number)

        for index in indexs:
            for j in range(len(c)):
                if index < c[j][0] or index == c[j][0]:
                    sentence = c[j][1]
                    wls = sentence.find(name)
                    sentence = sentence[wls:]
                    data.append(sentence)
                    break
        datas.append(data)
    max_len = len(datas[0])
    for i_add in range(len(datas)):
        repeat_part = ['non_content'] * (max_len - len(datas[i_add]))
        datas[i_add].extend(repeat_part)
    out_file = pd.DataFrame(np.array(datas))
    out_file.to_csv('jieba_result/'+out_name + str(filenum) + '.csv')


## 文章进行段落偏移并输出对应的句子中包含的单词 ##
def Vocabularies(filenum,content,result,out_name):
    a = Indexs(content, "。")
    b = content.split("。")
    #添加最后一行
    x=a[len(a)-1]
    y=len(b[len(b)-1])
    a.append(x+y)
    c=zip(a,b)
    c=list(c)
    datas=[]
    for name,number,indexs in result:
        data=[]
        data.append(name)
        data.append(number)
        for index in indexs:
            for j in range(len(c)):
                if index < c[j][0] or index == c[j][0]:
                    vocabularies=jiebaclearText(c[j][1],stopwords_directory)
                    data.append(vocabularies)
                    break
        datas.append(data)
    max_len = len(datas[0])
    for i_add in range(len(datas)):
        repeat_part = ['non_content'] * (max_len - len(datas[i_add]))
        datas[i_add].extend(repeat_part)
    out_file = pd.DataFrame(np.array(datas))
    out_file.to_csv(out_name + str(filenum) + '.csv')

## 文章进行段落偏移并输出对应的*****整个句子*****中包含的单词并获取趋势单词 ##
def ClearedVocabularies(filenum,content,result,out_name):
    a = Indexs(content, "。")
    b = content.split("。")
    #添加最后一行
    x=a[len(a)-1]
    y=len(b[len(b)-1])
    a.append(x+y)
    c=zip(a,b)
    c=list(c)
    datas=[]
    for name,number,indexs in result:
        data=[]
        data.append(name)
        data.append(number)

        for index in indexs:
            for j in range(len(c)):
                if index < c[j][0] or index == c[j][0]:
                    vocabularies=jiebaclearText(c[j][1],stopwords_directory)
                    vocabularies=jiebaclearVocabularies(vocabularies)
                    data.append(vocabularies)
                    break
        datas.append(data)
    max_len = len(datas[0])
    for i_add in range(len(datas)):
        repeat_part = ['non_content'] * (max_len - len(datas[i_add]))
        datas[i_add].extend(repeat_part)
    out_file = pd.DataFrame(np.array(datas))
    out_file.to_csv('jieba_result/'+out_name + str(filenum) + '.csv')



## 文章进行段落偏移并输出对应的从*****关键字*****开始的整个句子并获取趋势单词 ##
def NewClearedVocabularies(filenum,content,result,out_name):
    a = Indexs(content, "。")
    b = content.split("。")
    #添加最后一行
    x=a[len(a)-1]
    y=len(b[len(b)-1])
    a.append(x+y)
    c=zip(a,b)
    c=list(c)
    datas=[]
    for name,number,indexs in result:
        data=[]
        data.append(name)
        data.append(number)
        for index in indexs:
            for j in range(len(c)):
                if index < c[j][0] or index == c[j][0]:
                    sentence=c[j][1]
                    wls=sentence.find(name)
                    sentence=sentence[wls:]
                    vocabularies = jiebaclearText(sentence,stopwords_directory)
                    vocabularies = jiebaclearVocabularies(vocabularies)
                    data.append(vocabularies)
                    break
        datas.append(data)
    max_len = len(datas[0])
    for i_add in range(len(datas)):
        repeat_part = ['non_content'] * (max_len - len(datas[i_add]))
        datas[i_add].extend(repeat_part)
    out_file = pd.DataFrame(np.array(datas))
    out_file.to_csv('jieba_result/'+out_name + str(filenum) + '.csv')





## 输出对应的从*****关键字*****开始的整个句子并获取趋势单词和进行情感分类 ##
def NewClearedVocabulariesAndClassify(filenum,content,result,out_name):
    a = Indexs(content, "。")
    b = content.split("。")
    #添加最后一行
    x=a[len(a)-1]
    y=len(b[len(b)-1])
    a.append(x+y)
    c=zip(a,b)
    c=list(c)
    datas=[]
    resultlists = []
    for name,number,indexs in result:
        data=[]
        data.append(name)
        data.append(number)
        negative=0
        neutral=0
        positive=0
        resultlist=[]
        for index in indexs:
            for j in range(len(c)):
                if index < c[j][0] or index == c[j][0]:
                    sentence=c[j][1]
                    wls=sentence.find(name)
                    sentence=sentence[wls:]
                    data.append(sentence)
                    vocabularies = jiebaclearText(sentence,stopwords_directory)
                    vocabularieslist=jiebaclearVocabulariesandClassify(vocabularies)
                    newvocabularies=[]
                    if len(vocabularieslist)==0:
                        pass
                    else:
                        for vocabulary,classify in vocabularieslist:
                            newvocabularies.append(vocabulary)
                            if classify == -1:
                                negative+=1
                            elif classify == 0:
                                neutral+=1
                            elif classify == 1:
                                positive +=1
                        # data.append('/'.join(newvocabularies))
                    break
        resultlist.append('negative:'+str(negative)+'  '+'neutral:'+str(neutral)+'  '+'positive:'+str(positive))
        resultlists.append(resultlist)
        datas.append(data)
    max_len = len(datas[0])
    for i_add in range(len(datas)):
        repeat_part = ['non_content'] * (max_len - len(datas[i_add]))
        datas[i_add].extend(repeat_part)
        datas[i_add].extend(resultlists[i_add])
    out_file = pd.DataFrame(np.array(datas))
    out_file.to_csv('jieba_result/'+out_name + str(filenum) + '.csv')





## 输出对应从*****关键字*****开始的整个句子并使用textblob 对整个句子情感分析 ##
def NewSentencesAndClassify(filenum,content,result,out_name,out_len):
    a = Indexs(content, "。")
    b = content.split("。")
    #添加最后一行
    x=a[len(a)-1]
    y=len(b[len(b)-1])
    a.append(x+y)
    c=zip(a,b)
    c=list(c)
    datas=[]
    for name,number,indexs in result:
        data=[]
        data.append(name)
        data.append(number)

        for index in indexs:
            for j in range(len(c)):
                if index < c[j][0] or index == c[j][0]:
                    sentence = c[j][1]
                    wls = sentence.find(name)
                    sentence = sentence[wls:]
                    data.append(sentence)
                    data.append(str(TextBlob(sentence).sentiment))
                    break
        datas.append(data)
    max_len = len(datas[0])
    for i_add in range(len(datas)):
        repeat_part = ['non_content'] * (max_len - len(datas[i_add]))
        datas[i_add].extend(repeat_part)
    out_file = pd.DataFrame(np.array(datas))
    out_file.to_csv('textblob_result/'+out_name + str(filenum) + '.csv')




## 并输出对应的从*****关键字*****开始以“，”结束，并分为5个单词，不足5个，以当前词数为主 ##
## 分析趋势单词，确定每个单词各个句子的情感，并针对各个句子的情感对该单词进行汇总 ##
def LastNewClearedVocabulariesAndClassify(filename,content,result,top_ideas,split_content,stopwords_directory):

    ## 提取文本 作者、日期、题目等 信息 ##
    author = []
    first_sentence = filename
    start_index = first_sentence.find('【')
    end_index = first_sentence.find('】')
    orginization_index = first_sentence.find('-')
    author = first_sentence[orginization_index + 1:end_index]
    originization = first_sentence[start_index + 1:orginization_index]
    title = first_sentence[end_index + 1:]
    single_information = [first_sentence,title, author, originization
                          ]

    ## 提取研报发布的 日期  ##
    contents = split_content.split("/")
    for cont in contents:
        if '年' in cont and '月' in cont and len(cont) >= 7:
            single_information.append(cont)
            break


    a = Indexs(content, "。")
    b = content.split("。")
    x=a[len(a)-1]
    y=len(b[len(b)-1])
    a.append(x+y)
    c=zip(a,b)
    c=list(c)
    datas=[]
    resultlists = []

    ## 若初步分词结果为 空，不进行 不许操作 ##
    if len(result)==0:
        print('extracting nothing from the papers')
        return []
    else:
        for name,number,indexs in result:
            data=[]
            data.append(name)
            data.append(number)
            resultlist=[]
            neg=0
            neu=0
            pos=0
            for index in indexs:
                negative = 0
                neutral = 0
                positive = 0
                for j in range(len(c)):
                    #print(c[j])
                    if index < c[j][0] or index == c[j][0]:
                        sentence=c[j][1]
                        length=c[j][0]-index
                        newindex=(len(sentence)-length-1)
                        sentence=sentence[newindex:]
                        wls0=sentence.find(name)
                        wls0=wls0+len(name)
                        sentence = sentence[wls0:]
                        wls1 = sentence.find("，")
                        if wls1 ==-1:
                           pass
                        else:
                            sentence = sentence[:wls1]
                        ## 删除类似图+数字后面的无意义内容 ##
                        delete_tu=[]
                        for i_tu in range(1,100):
                            delete_tu.extend(['图'+str(i_tu),'表'+str(i_tu)])
                        delete_tu.extend(['资料来源','敬请阅读','宏观经济','wind'])

                        for i_delete in delete_tu:
                            if sentence.find(i_delete)!=-1:

                                sentence=sentence[:sentence.find(i_delete)]

                        data.append(sentence)
                        vocabularies = jiebaclearText(sentence,stopwords_directory)
                        vocabularies=vocabularies.split("/")
                        if len(vocabularies)<6:
                            pass
                        else:
                            vocabularies=vocabularies[:5]
                        vocabularies = "/".join(vocabularies)
                        vocabularieslist = jiebaclearVocabulariesandClassify(vocabularies)
                        newvocabularies=[]
                        if len(vocabularieslist)==0:
                            data.append('negative:'+str(0)+'  '+'neutral:'+str(0)+ '  ' +'positive:'+str(0))
                            data.append('none')
                        else:
                            for vocabulary,classify in vocabularieslist:
                                newvocabularies.append(vocabulary)
                                if classify == -1:
                                    negative+=1
                                elif classify == 0:
                                    neutral+=1
                                elif classify == 1:
                                    positive +=1
                            data.append('negative:'+str(negative)+'  '+'neutral:'+str(neutral)+'  '+'positive:'+str(positive))
                            mark=negative*(-1)+neutral*0+positive*1
                            if mark < 0:
                                neg+=1
                                data.append('negative')
                            elif mark >0:
                                data.append('positive')
                                pos+=1
                            else:
                                data.append('neutral')
                                neu+=1
                        break

            resultlist.extend(['negative:',str(neg)])
            resultlist.extend(['neutral:',str(neu)])
            resultlist.extend(['positive:',str(pos)])
            resultlists.append(resultlist)
            datas.append(data)

        ## 填充 空的内容到data 保持size 一致，好直接生成data frame ##
        max_len = len(datas[0])
        max_occur=int(datas[0][1])

        for i_add in range(len(datas)):
            tuple=int((max_len - len(datas[i_add])) / 3)
            repeat_part = ['non_content','none_statistics','none_type'] * tuple
            datas[i_add].extend(repeat_part)
            datas[i_add].extend(resultlists[i_add])

        ## 删除 积极、消极统计 全为零的 合成词 以及相应数据 ##
        datas=list(filter(lambda x: x[-1]!='0' or x[-5]!='0',datas))

        ## 加入结论 及相应索引 便于管理dataframe ##
        for i_con in range(len(datas)):
            if datas[i_con][-3]>=datas[i_con][-1] and datas[i_con][-3]>=datas[i_con][-5]:
                datas[i_con].extend(['delete',datas[i_con][0]+'delete'])
            elif datas[i_con][-5]>datas[i_con][-1]:
                datas[i_con].extend(['down',datas[i_con][0]+'下降'])
            elif datas[i_con][-5]<datas[i_con][-1]:
                datas[i_con].extend(['up',datas[i_con][0]+'上升'])
            else:
                datas[i_con].extend(['flat',datas[i_con][0]+'保持平稳'])

        ##  删除 中立观点居多的 无意义数据 ##
        datas=list(filter(lambda x: x[-2]!='delete',datas))

        if len(datas)!=0:
        # 接着 经过上述筛选 再判定 是否 提取的datas 为空 #
            # 删除 上述 索引的列 #
            datas = np.array(datas).T.tolist()
            del datas[-2]
            datas=np.array(datas).T.tolist()

            non_sense_list_word = ['宏观研究所', '中国经济评论','证券研究','安信证券',
                                    '中国宏观专题报告','全国城镇调查',
                                   '大城市城镇调查','依然占据主导',
                                   '同比少增7863','逻辑不像2017','典型扩张变为',
                                   '扩张变为高位','茅台景气度受','景气度受房价'
                                   ,'证券发展','研究中心','敬请阅读末页']

            # 删除一些无实际意义的合成词 有经验所得 #
            for i_row in range(len(datas)):
                for i_non_sense in non_sense_list_word:
                    if i_non_sense in datas[i_row][0]:
                        datas[i_row].append('delete')
                        break
                else:
                    datas[i_row].append('keep')


            datas=list(filter(lambda x: x[-1]!='delete',datas))
            datas = np.array(datas).T.tolist()

            # 删除最后一列的 状态词 #
            del datas[-1]
            datas=np.array(datas).T.tolist()


            # 只提取 top idea 的数据 包括 结论 #
            if top_ideas>=len(datas):
                datas=datas
            else:
                datas=datas[:top_ideas]

            # 每篇研报 得出的 结论 和发布信息(日期 作者等)整合在一起 #
            take_con=datas
            take_con=np.array(take_con).T[-1].tolist()
            repeat_time=len(take_con)
            single_information=np.repeat(np.array(single_information),repeat_time,axis=0)
            single_information=np.reshape(single_information,
                                          [-1,repeat_time]).tolist()
            extraction_result=np.array(single_information+[take_con]).T



            # 创建dataframe 为 研报里 提取出的 所有的 词语 句子 及统计结果 #
            # 创建dataframe名称 #
            sub_column_1=['提取的句子','情绪词统计','情绪结果']*max_occur
            sub_column_2=['消极','结果统计','中立','结果统计','积极','结果统计','结论']
            column=['合并短语','出现次数']
            column.extend(sub_column_1)
            column.extend(sub_column_2)

            out_file = pd.DataFrame(np.array(datas),columns=column)
            out_file.to_csv('extraction_research_papers/'+filename + '.csv',
                            encoding='utf_8_sig')

            return extraction_result
        else:
            return []


## 2018_05_31  将从所有研报中提取出的 结论 和发布信息 整合在一起 ##
def obtain_conclusion(file_directory,top_idea,Counts,stopwords_directory):
    #
    filenum = 1
    files = RF.file_names(file_directory)
    print("需要处理的文件数目为{0}".format(len(files)))
    print("执行进度:")
    print("start.................................")
    collection=[]
    for file in files:
        content = file[1]
        filename = file[0]
        clearedcontent = jiebaclearText(content,stopwords_directory)
        recontent = restructureword(clearedcontent, 3)
        result = TopN(content, recontent,Counts)
        print('***********' + filename + '*************')
        #print(result)
        print('***********' + filename + '*************')
        ## 选取的关键点的 个数 ##
        # print(result)
        # NewSentences(filenum,content,result,out)
        # Vocabularies(filenum, content, result, out)
        # ClearedVocabularies(filenum, content, result, out)
        # NewClearedVocabularies(filenum,content,result,out)
        # NewClearedVocabulariesAndClassify(filenum,content,result,out)
        extraction_result=LastNewClearedVocabulariesAndClassify(filename,
                                                                content, result,
                                                                top_idea, clearedcontent,
                                                                stopwords_directory)
        #print('the extraction....result',len(extraction_result))#,#extraction_result)
        collection.extend(extraction_result)
        print("file" + str(filenum) + " finished")
        filenum += 1

    print("end...................................")
    #print('the collection....',collection)
    # 列的名称 #
    final_column=['研报名称','标题','作者','发布机构','日期','相应结论']

    collection=pd.DataFrame(collection,columns=final_column)
    collection.to_csv('extraction_research_papers/研报提取内容汇总.csv',encoding='utf_8_sig')


if __name__ =="__main__":
    ## 得到最终的研报提取结果 ##

    # 处理的研报指定的目录 #
    #file_directory = "research_paper"

    # 停用词相对路径
    stopwords_directory = "add_vocabulary/stopwords.txt"
    trend_directory = "add_vocabulary/trend_term.txt"
    # 设置的 最多提取的结论 从每篇研报中 #
    #top_number = 10
    # 提取的词 在原文中至少出现过的次数 #
    #Counts = 2
    #obtain_conclusion(file_directory, top_number, Counts,stopwords_directory)
