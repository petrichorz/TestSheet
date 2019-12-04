import numpy as np
import pandas as pd
import re
import bktree as bk
import math

def is_number(num):
    pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
    result = pattern.match(num)
    if result:
        return True
    else:
        return False


def cal_used_editdistance(word):
    EditDistance = math.floor(0.25 * len(word))
    return EditDistance if EditDistance > 0 else 1


class Treeobj(object):

    def __init__(self, dict):
        self.bktree = bk.BKTree()
        for strobj in dict:
            strobj = strobj.rstrip('[\n\r]')
            self.bktree.insert(bk.StringObject(strobj))

    def is_error(self, str):
        for obj in self.bktree.find(bk.StringObject(str), 0):
            return False
        return True

    def FuzzyMatch_v1(self, str, lsNum):
        outputlist = []
        flag = 0
        for obj in self.bktree.find(bk.StringObject(str), lsNum):
            flag += 1
            outputlist.append(obj.value)
        return outputlist
    
    def add_dict(self, dict):
        for strobj in dict:
            strobj = strobj.rstrip('[\n\r]')
            self.bktree.insert(bk.StringObject(strobj))

    '''
    str is the string need to fuzzy match
    reverse decide whether sort the output and output the len equal to str itself
    怕看不懂
    str 是待匹配字符串
    reverse决定是否只要输出长度一样的
    当然如果没有长度一样的，会全部输出
    '''
    # 外层封装结构，调用这个
    def FuzzyMatch_v2(self, str="", reverse=True):
        # 洗掉无意义的浮点数
        if is_number(str) or not self.is_error(str):
            #print("meaningless fuzzy match")
            '''这里以后可以替换为打印到log'''
            return
        match_str = self.FuzzyMatch_v1(str, cal_used_editdistance(str))
        '''
        根据是否对reverse为False时进行排序，看是否要取消注释
        if len(match_str) > 1:
            match_str.sort(
                key=lambda i: abs(len(i)-len(str)), reverse=False)
        '''
        match_str_filter = list(filter(lambda i: len(i) == len(str), match_str)) if reverse else match_str
        #过滤掉长度不一样的
        output = match_str_filter if len(match_str_filter) > 0 else match_str
        #如果没有长度不一样的，全部输出
        return output

'''
不会用看这个
'''
if __name__ == "__main__":
    #str = input("输入待匹配项:")
    #lsNum = input("编辑距离:")
    print("-----------------------------")
    print("匹配结果如下:")
    To = Treeobj(['青海省', '内蒙自治区', '内古自治区', '内蒙古自治区',
                  '西藏自治区', '新疆维吾尔自治区', '广西壮族自治区'])
    print(To.FuzzyMatch_v2(str="内x古自治区", reverse=False))
    print(To.FuzzyMatch_v2(str="内x古自治区", reverse=True))
