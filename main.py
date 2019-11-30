import readxls as rx
import re
import math
import datetime

inputFilePath = "./error_word.txt"
outputFilePath = "./error_out.txt"
rightwordPath = "./rightword.txt"
errorwordPath = "./errorword.txt"
EditDistance = 2


def is_number(num):
    pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
    result = pattern.match(num)
    if result:
        return True
    else:
        return False


def is_error(bktree, str):
    return bktree.is_error(str)

def cal_editdistance(word):
    EditDistance = math.floor(0.25 * len(word))
    return EditDistance if EditDistance > 0 else 1

bktree = rx.Treeobj('./dict.xls', outputFilePath)
right = open(rightwordPath, 'w')
wrong = open(errorwordPath, 'w')

start = datetime.datetime.now()
for word in open(inputFilePath, 'r'):
    word = word.rstrip('[\n\r]')
    if not is_number(word):
        if is_error(bktree, word):
            print(word + " have error\n")
            wrong.write(word + " have error\n")
        else:
            print(word + " no error\n")
            right.write(word + " have no error\n")
            continue
        # 洗掉所有浮点数，浮点数匹配感觉没有意义
        print("\n"+word)
        bktree.FuzzyMatch(word, cal_editdistance(word))
        print("----------------------------------------------------")
    else:
        continue
end = datetime.datetime.now()
print(end-start)