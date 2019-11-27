import readxls as rx
import re

inputFilePath = "./error.txt"
outputFilePath = "./errot_out.txt"
EditDistance = 2


def is_number(num):
    pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
    result = pattern.match(num)
    if result:
        return True
    else:
        return False


bktree = rx.Treeobj('./dict.xls', outputFilePath)

for word in open(inputFilePath, 'r'):
    if not is_number(word):
        print("\n"+word)
        bktree.FuzzyMatch(word, EditDistance)
        print("----------------------------------------------------")
    else:
        continue
