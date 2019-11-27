from Levenshtein import distance
import numpy as np

class BKTree(object):
    def __init__(self):
        self.root = None
        pass

    def insert(self, obj):
        if self.root == None:
            self.root = BKNode(obj)
        else:
            self.root.insert(obj)

    def find(self, obj, threshold):
        if self.root is not None:
            for res in self.root.find(obj, threshold):
                yield res

    def __str__(self):
        return 'BKTree<root:%s>' % (self.root)


class BKNode(object):
    obj = None
    children = dict()

    def __init__(self, obj):
        self.obj = obj
        self.children = dict()

    def insert(self, obj):
        if obj.value == self.obj.value:
            return False
        else:
            d = obj.distance(self.obj)
            if d in self.children.keys():
                self.children[d].insert(obj)
            else:
                self.children[d] = BKNode(obj)
            return True

    def find(self, obj, threshold):
        d = obj.distance(self.obj)
        if d <= threshold:
            yield self.obj

        dmin = d-threshold
        dmax = d+threshold
        for i in range(dmin, dmax+1):
            if i in self.children.keys():
                for child in self.children[i].find(obj, threshold):
                    yield child

    def __str__(self):
        children_str = ''
        for k in self.children:
            children_str = '%s[%s,%s]' % (
                children_str, k, self.children[k].__str__())
        if children_str == '':
            children_str = '[]'
        return 'BKNode<obj:%s, children:%s>' % (self.obj, children_str)


class StringObject(object):
    def __init__(self, value):
        self.value = value

    def distance(self, obj):
        return distance(self.value, obj.value)

    def get(self):
        return self.value

    def __str__(self):
        return '    %s' % (self.value)


if __name__ == "__main__":
    bktree = BKTree()
    bktree.insert(StringObject('乙醇'))
    bktree.insert(StringObject('乙醇'))
    print(bktree)
