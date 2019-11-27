import numpy as np
import pandas as pd
import re
import bktree as bk


class Treeobj(object):
    keyword = ['简称', '项目名称', '单位', '参考值', '检测方法']
    bktreeList = []
    outputfilePath = ""

    def __init__(self, fp, op):
        frame = pd.read_excel(fp)
        index = 0
        self.outputfilePath = op

        for strIndex in self.keyword:
            frame_list = frame[strIndex]
            frame_data = frame_list.dropna(how='all')

            locals()['bktree_'+strIndex] = bk.BKTree()

            for strobj in frame_data:
                strobj = strobj.rstrip('[\n\r]')
                strobj = re.sub('[\n\r\t]', ' ', strobj)
                locals()['bktree_'+strIndex].insert(bk.StringObject(strobj))

            self.bktreeList.append(locals()['bktree_'+strIndex])
            index += 1

    def FuzzyMatch(self, str, lsNum):
        outputfile = open(self.outputfilePath, "a")
        index = 0
        flag = 0
        outputfile.write("\n待匹配项:"+str)
        outputfile.write("-------------------------\n")
        for tree in self.bktreeList:
            print(self.keyword[index]+':')
            outputfile.write(self.keyword[index]+':\n')
            for obj in tree.find(bk.StringObject(str), lsNum):
                flag += 1
                print(obj)
                outputfile.write("  "+obj.value+'\n')
            if flag == 0:
                print(" 结果为空")
                outputfile.write("  结果为空\n")
            flag = 0
            index += 1


if __name__ == "__main__":
    str = input("输入待匹配项:")
    lsNum = input("编辑距离:")
    print("-----------------------------")
    print("匹配结果如下:")
    To = Treeobj("./dict.xls", "./output.txt")
    To.FuzzyMatch(str, int(lsNum))
