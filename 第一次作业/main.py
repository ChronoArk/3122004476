import jieba    #中文分词
import sys      #命令行

#利用jaccard比较两个文件的相似度
def Jaccard(model,reference):#refenrence为原文件，model为抄袭文件
    # 将中文字符串用jieba进行精确分词
    terms_refenrence = jieba.cut(reference,cut_all=False)
    terms_model = jieba.cut(model,cut_all=False)
    grams_reference =  set(terms_refenrence) #去重
    grams_model = set(terms_model)
    temp = 0
    for i in grams_reference:
        if i in grams_model:
            temp += 1
    merge = len(grams_model)+len(grams_reference)-temp #并集
    jaccard_coefficient = float(temp/merge) #交集
    return jaccard_coefficient

#读写文件
def file():
    if len(sys.argv) != 4:
        print("错误。正确格式：python main.py 原文文件路径 抄袭文件路径 输出文件路径")
        sys.exit(1)
    with open(sys.argv[1],'r',encoding='utf-8') as f:
        f1 = f.read()   #打开原文件，写入f1
    with open(sys.argv[2],'r',encoding='utf-8') as f:
        g1 = f.read()   #打开抄袭文件，写入g1

    similarity = Jaccard(f1,g1) #计算相似率

    with open(sys.argv[3], 'a', encoding='utf-8') as f:
        f.write( "{:.2f}\n\n".format( similarity ) ) #将相似率写入答案文件中

if __name__ == '__main__':
    file()
