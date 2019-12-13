import FuzzyMatch as fm
import pandas as pd
import numpy as np
import re

def remove_punctuation(str):
    filter_relu = re.compile(u"[^↓↑μ.,\^/\\a-zA-Z0-9\u4e00-\u9fa5\uFF01-\uFF64\u3000-\u303F\uFE10-\uFE1F]")
    #先把字符串转为unicode编码
    str = filter_relu.sub('',str)
    return str

def filter_list(strlist):
    filtered = []
    for obj in strlist:
        filtered.append(remove_punctuation(obj))
    return filtered

class Classification(object):
    bktreeList = []

    def __init__(self, fp):
        frame = pd.read_excel(fp)
        self.keyword = list(frame)
        for strIndex in self.keyword:
            frame_list = frame[strIndex]
            frame_data = frame_list.dropna(how='all')  # 清洗nan
            locals()['bktree_'+strIndex] = fm.Treeobj(frame_data)  # 利用内层接口构建bk
            self.bktreeList.append(locals()['bktree_'+strIndex])  # 将树插入森林

    def dict_increase(self, Classification, dict):
        index = self.keyword.index(Classification)
        if index >= 0:
            self.bktreeList[Classification].add_dict(dict)
        else:
            self.keyword.append(Classification)
            locals()['bktree_'+Classification] = fm.Treeobj(dict)  # 利用内层接口构建bk
            self.bktreeList.append(
                locals()['bktree_'+Classification])  # 将树插入森林
        # 向现有树内新增字典功能

    # 然后需要判断送入的一个单词是哪一类
    '''
    我想的是在这里做一个投票策略，先给每一项可能出现的列都形成一个array,最后求个众数就行
    所以第一步是找到每一个str可能出现的列
    '''

    def str_score(self, str):
        strLabel = []
        index = 0
        for tree in self.bktreeList:
            if not tree.is_error(str):
                #is_error本意是产看str在树tree中有没有
                strLabel.append(index)
            index += 1
        if len(strLabel) == 0:
            index = 0
            for tree in self.bktreeList:
                result = tree.FuzzyMatch_v1(str, fm.cal_used_editdistance(str))
                for i in range(len(result)):
                    strLabel.append(index)
                index += 1
        return strLabel
    # 这代码太丑了，后面再重构吧，这一堆的for看的我头痛

    '''
    然后对刚才的进行外层封装，送入一个list形成投票
    '''

    def list_vote(self, strlist):
        votebox = []
        for strobj in strlist:
            if fm.is_number(strobj) or fm.is_null(strobj):
                continue
            votebox.extend(self.str_score(strobj))
        # 形成投票箱后进行投票
        if len(votebox) == 0:
            return "unknowed"
        voteboard = np.bincount(votebox)
        # 先获取出现次数列表
        return self.keyword[np.argmax(voteboard)]

    #懒人专用接口，直接给list,返回dict
    def sheet_divide(self, sheetlist):
        titlelist = []
        obfuscation = ["结果","参考值"]
        switch =  0
        #做个二项开关
        for list in sheetlist:
            #dict[self.list_vote(list)] = list
            if self.list_vote(list) in ['unknowed','参考值']:
                title = obfuscation[switch]
                switch = not switch
            else:
                title = self.list_vote(list)
            titlelist.append(title)
        return titlelist


if __name__ == "__main__":
    # 给你个调试接口
    classtest = Classification("./dict.xls")
    testlist = [['LYM', 'CD19+', 'CD4+', 'CD3+%', 'CD8+%', 'CD4/CD8'],
                ['淋巴细胞总数', '总B淋巴细胞数', '辅助性T细胞数','总T淋巴细胞%', '抑制/细胞毒性T细胞%', 'CD4/CD8比值'],
                ['00', '108', '496', '76.37', '22.30', '2.22'],
                ['↓', 'null', 'null', 'null', 'null', 'null'],
                ['M/L', 'M/L', 'M/L', '%', '%', 'null'],
                ['1200-3400', '90-323', '410-884','50.00-84.00', '15.00-44.00', '0.71-2.87'],
                ['CD3+', 'CD8+', 'CD3-CD16+CD56+','CD19+%', 'CD4+%', 'CD3-CD16+CD56+%'],
                ['总T淋巴细胞数', '抑制/细胞毒性T细胞数', 'NK细胞数', '总B淋巴细胞%', '辅助性T细胞%', 'MK细胞%'],
                ['764', '223', '90', '10.83', '49.58', '9.03'],
                ['M/L', 'M/L', 'M/L', '%', '%', '%'],
                ['690-1760', '190-658', '90-536','5.00-18.00', '27.00-51.00', '7.00-40.00']
                ]
    testlist2 = [['↓', 'null', 'null', 'null', 'null', 'null']]
    print(classtest.sheet_divide(testlist))
    classtest.sheet_divide(testlist2)
    '''
    listline=[['Pb', 'Zn(Q)', 'Cu(Q)', 'Fe(Q)', 'Ca(Q)', 'Mg(Q)'], ['全血铅', '全血锌', '全血铜', '全血铁', '全血钙', '全血镁'], ['25', '103.68', '35.13', '8.33', '1.53', '1.37'], ['μg/L', 'μ■ol/L', 'μmol/L', '■mol/L', '■mol/L', '■mol/L'], ['0-200', '76.50-170.00', '11.80-39.30', '7.52-11.82', '1.31-1.95', '1.12-2.06']]
    listline2=[['T3', 'T4', 'FT3', 'FT4', 'TSH', 'TG-Ab', 'TP0-Ab'], ['三碘甲状腺原氨酸', '甲状腺素', '游离三碘甲状腺原氨酸', '游离甲状腺素', '促甲状腺激素', '抗甲状腺球蛋白抗体', '抗甲状腺过氧化物酶抗体'], ['4.76', '205.80', '16.54', '51.60', '<0.005', '486.80', '302.00'], ['↑', '↑', '↑', '↑', '↓', '↑', '↑'], ['nmol/t', 'nmol/L', 'pmol/L', 'pmol/L', '■IU/L', 'KIU/L', 'KIU/L'], ['1,30-3.10', '66.00-181.00', '3.10-6.80', '12.00-22.00', '0.270-4.200', '<115.00', '<34.00']]
    for list1 in listline2:
        print(filter_list(list1))
    '''