#!/usr/bin/python

data = [ '25', '52', '164', '240', '274', '328', '368', '448', '538', '561', '630', '687', '730', '775', '825', '834' ]

minsup = 5
rawDict = {}

for trans in data:
    items = list(trans)
    for item in items:
        rawDict[item] = rawDict.get(item, 0) + 1
# rawDict => {'1': 2, '0': 3, '3': 6, '2': 6, '5': 6, '4': 6, '7': 5, '6': 5, '8': 7}

for key in rawDict.keys():
    if rawDict[key] <= minsup :
        del rawDict[key]    
# rawDict => {'3': 6, '2': 6, '5': 6, '4': 6, '8': 7}

# TODO1: sort rawDict by key alphabetically and then value
orderedFreqItems = [v[0] for v in sorted(sorted(rawDict.items(), key=lambda q:q[0], reverse=False), key=lambda p: p[1], reverse=True)]
# orderedFreqItems => ['8', '2', '3', '4', '5']

# TODO2: create class for 'tree'
class tree:
    def __init__(self, itemName, parent, count):
        self.itemName = itemName
        self.parent = parent
        self.count = count
        self.children = {}

    def getName(self):
        if self != None:
            return self.itemName
        return " - "

    def toString(self):
        print "Name-" + self.itemName + " : count-" + str(self.count)
        #  + " : Parent-" + self.parent.itemName
        # print children
        if self.children:
            # print self.children 
            for childName in self.children:
                print childName 

# TODO3: create fp-tree based on database
# TODO4: create conditional fp-tree based on fp-tree
print orderedFreqItems
root = tree('root', None, 0)

# incorrect: create treeNode for all frequent items and make them as child of 'root'
for item in orderedFreqItems:
    root.children[item] = tree(item, root, 0)

root.toString()


