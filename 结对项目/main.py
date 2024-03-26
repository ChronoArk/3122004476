from fractions import Fraction as Frac
import random
import sys
import re
from time import *  #时间统计库

def outnumber(limit):  # 产生所需数字列表和运算符个数
    sign_num = random.randint(1, 3)  # 随机产生运算符的个数
    operate_num = sign_num + 1  # 式子中运算的个数
    fraction_num = random.randint(0, operate_num)  # 随机产生式子中有多少个分数
    need_num = operate_num + fraction_num  # 所需要的数字个数
    numbers = [random.randint(1, limit) for _ in range(need_num)]  # 产生不大于r的随机数列表
    if fraction_num != 0:  # 判断有无分数
        up = None  # 分子分母
        bom = None
        for i in range(fraction_num):  # 产生fraction_num个分数
            for number in numbers:  # 找非零的数
                if number != 0:
                    up = number
                    numbers.remove(number)
                    break
            for number in numbers:
                if number != 0:
                    bom = number
                    numbers.remove(number)
                    break
            frac = Frac(up, bom)  # 计算分数
            if frac.denominator == 1:  # 判断分母是否为1
                frac = frac.numerator
            numbers.append(frac)  # 暂存到add中
    return sign_num, numbers


def text(limit):  # 产生一道题目
    sign_num, num_list = outnumber(limit)
    tmp_list = list()
    for i in num_list:  # 查找分数
        if isinstance(i, Frac):  # 加括号使分数优先运算
            tmp_list.append('('+str(i)+')')
        else:  # 非分数直接加入
            tmp_list.append(i)
    num_list = tmp_list
    for i in range(sign_num, 0, -1):  # 插入运算符
        place = i
        sign = random.choice(['+', '-', '*', '/'])
        num_list.insert(place, sign)  # 包含运算符的列表
    expression = " ".join(map(str, num_list))  # 转化成一个字符串并计算结果
    result = eval(expression)  # 若为分数就是float
    if not isinstance(result, int):
        result = Frac(result).limit_denominator()  # 计算式子的值并转换为分数
    return result, num_list  # 输出数字和符号


def request_format(org):  # 转换成所要求的格式
    change = list()
    use_sign = ['+', '-', '*', '/', '=']
    print_sign = ['\u002B', '\u2212', '\u00D7', '\u00F7', '=']
    for i in org:
        if i in use_sign:  # 转换为书写体的符号
            index = use_sign.index(i)
            change.append(print_sign[index])
        else:  # 转化数字为要求格式
            if isinstance(i, str):  # 转化分数
                item = Frac(eval(i)).limit_denominator()
                if item > 1 and item.denominator != 1:  # 转换为真分数
                    integer_part = item // 1  # 得到整数部分
                    proper_fraction = item % 1  # 得到真分数部分
                    change.append("{}\'{}".format(integer_part, proper_fraction))
                else:  # 原本为真分数
                    change.append("{}".format(item))
            else:  # 非分数
                change.append(i)
    change = " ".join(map(str, change))  # 转换成字符串
    return change


def make_questions(num, limit):  # 产生题目
    no = 1  # 题目序号
    text_list = dict()  # 整条等式
    answer_list = dict()  # 答案部分
    question_list = dict()  # 问题部分
    while no <= num:  # 循环产生num个题目
        res, num_list = text(limit)
        if res < 0 or res > limit or res.denominator > limit:  # 若结果为0、大于r分母大于r则重新生成
            continue
        else:
            tag = 0  # 标记是否重复
            question = request_format(num_list)
            num_list.append("=")
            num_list.append((str(res)))
            exp = request_format(num_list)
            for i in text_list:  # ------------但生成式子多时效率很低------换种查找
                if text_list.get(i) == question:  # 判断是否有相同的式子后加入
                    tag = 1
            if tag == 1:  # 判断是否新增题目
                continue
            else:  # 新增题目
                text_list[no] = question
                question_list[no] = exp
                if res > 1 and res.denominator != 1:  # 转换为真分数
                    integer_part = res // 1  # 得到整数部分
                    proper_fraction = res % 1  # 得到真分数部分
                    res = "{}\'{}".format(integer_part, proper_fraction)
                answer_list[no] = res
                no += 1

    return [text_list, answer_list, question_list]  # 返回整个等式 答案 问式


def check(did, answer, num):  # 判断对错
    """
    哥们认为你是搞成这样：{1:"答案"} 1是数字
    应该是文件一行读取readline 去除换行
    用spilt    例如："1.4‘1/2".spilt(".")
    eval函数可以把字符串变成数字
    """
    correct_total = 0
    wrong_total = 0
    correct = tuple()
    wrong = tuple()
    for i in range(num):  # 对照答案统计
        if did[i+1] == answer[i+1]:
            correct_total += 1
            correct += (i+1,)
        else:
            wrong_total += 1
            wrong += (i+1,)
    correct_print = ''.join(map(str, ["Correct:", correct_total, correct]))
    wrong_print = ''.join(map(str, ["Wrong:", wrong_total, wrong]))
    return correct_print, wrong_print

#将问题写入Exercises.txt，答案写入Answer.txt
def file(num,limit):
    startT = time()             #起始时间
    bag = make_questions(num,limit) #bag取make_questions的返回值列表
    with open('Exercises.txt','w',encoding='utf-8') as f:   #问题
        for i in range(num):
            question = bag[0][i+1]      #bag[0]是问题字典
            f.write("{}. {}\n".format(i+1,question))
    with open('Answer.txt','w',encoding='utf-8') as k:      #答案
        for i in range(num):
            answer = bag[1][i+1]        #bag[1]是答案字典
            k.write("{}. {}\n".format(i+1,answer))
    with open('test.txt','w',encoding='utf-8') as g:        #整式
        for i in range(num):
            test = bag[2][i+1]          #bag[2]是整式字典
            g.write("{}. {}\n".format(i+1,test))

    endT = time()               #终止时间
    print("time = %.2g 秒\n" % (endT - startT))

    dict_keys = list(bag[1].keys())
    random.shuffle(dict_keys)
    new_dict = {}
    for key in dict_keys:
        new_dict[key] = bag[1].get(key)
    cro,wro = check(new_dict,bag[1],num)
    with open('Grade.txt','w',encoding='utf-8') as h:
        h.write("{}\n{}".format(cro,wro))

def main():
    str_input = ''
    for i in range(1, len(sys.argv)):
        str_input += sys.argv[i]
    num_arg = '-n([\d]+)'
    limit_arg = '-r([\d]+)'
    num = int(re.search(num_arg,str_input).group(1))
    limit = int(re.search(limit_arg,str_input).group(1))
    if (num <= 0) or (limit <= 0):
        print("[-]参数错误")
        print("exiting")
        return
    else:
        file(num,limit)
        return 0

if __name__ == "__main__":
    main()
