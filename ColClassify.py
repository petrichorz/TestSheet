import FuzzyMatch as fm
import pandas as pd
import numpy as np


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
            if fm.is_number(strobj):
                continue
            votebox.extend(self.str_score(strobj))
        # 形成投票箱后进行投票
        if len(votebox) == 0:
            return "UnknowCol"
        voteboard = np.bincount(votebox)
        # 先获取出现次数列表
        return self.keyword[np.argmax(voteboard)]


if __name__ == "__main__":
    # 给你个调试接口
    classtest = Classification("./dict.xls")
    testlist = [['LYM', 'CD19+', 'CD4+', 'CD3+%', 'CD8+%', 'CD4/CD8'],
                ['淋巴细胞总数', '总B淋巴细胞数', '辅助性T细胞数','总T淋巴细胞%', '抑制/细胞毒性T细胞%', 'CD4/CD8比值'],
                ['00', '108', '496', '76.37', '22.30', '2.22'], 
                ['↓', 'null', 'null', 'null', 'null', 'null'], 
                ['M/L', 'M/L', 'M/L', '%', '%', 'null'], 
                ['1200-3400', '90-323', '410-884', '50.00-84.00', '15.00-44.00', '0.71-2.87'], 
                ['CD3+', 'CD8+', 'CD3-CD16+CD56+', 'CD19+%', 'CD4+%', 'CD3-CD16+CD56+%'], 
                ['总T淋巴细胞数', '抑制/细胞毒性T细胞数', 'NK细胞数', '总B淋巴细胞%', '辅助性T细胞%', 'MK细胞%'], 
                ['764', '223', '90', '10.83', '49.58', '9.03'], 
                ['M/L', 'M/L', 'M/L', '%', '%', '%'], 
                ['690-1760', '190-658', '90-536', '5.00-18.00', '27.00-51.00', '7.00-40.00']
    ]
    testlist2 = ['764', '223', '90', '10.83', '49.58', '9.03']
    for list in testlist:
        print(classtest.list_vote(list),end=' ')
    print("\n")
    '''
    print(classtest.list_vote(testlist2))
    '''