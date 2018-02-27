#!/usr/bin/python

data = [ '25', '52', '164', '240', '274', '328', '368', '448', '538', '561', '630', '687', '730', '775', '825', '834' ]

minsup = 5
freqItemsDict = {}  # {'3': 6, '2': 6, '5': 6, '4': 6, '8': 7}  only those above the threshold
rawDict = {}    # { frozenset(['2','5']): 2, frozenset(['1','4', '6']): 1 ... }

# prepare data
for trans in data:
    print list(trans)
    # print "trans" + list(trans) + str(type(trans))
    rawDict[tuple(trans)] = rawDict.get(tuple(trans), 0) + 1
    for item in trans:
        freqItemsDict[item] = freqItemsDict.get(item, 0) + 1

# filter out candidate of length 1 which are below threshold
for key in freqItemsDict.keys():
    if freqItemsDict[key] <= minsup :
        del freqItemsDict[key]    

# TODO1: sort rawDict by key alphabetically and then value
orderedFreqItemsBySupport = [v[0] for v in sorted(sorted(freqItemsDict.items(), key=lambda q:q[0], reverse=False), key=lambda p: p[1], reverse=True)]
print orderedFreqItemsBySupport
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

    def toString(self, indentation):
        print indentation + "Name-" + self.itemName + " : count-" + str(self.count)
        #  + " : Parent-" + self.parent.itemName
        # print self.children
        if self.children:
            # print self.children 
            for childName in self.children:
                # print childName +" : "+str(self.children[childName].count)
                self.children[childName].toString(indentation + "-")

    def inc(self,counter):
        self.count = self.count + counter

# accept a list of frequent items and update the fp-tree
def updateTree(items, parentTree, count):
    print "updateTree is called - "+parentTree.getName()+" : "+str(count)
    print items
    print "------------------------------------------------"
    if items[0] in parentTree.children:
        parentTree.children[items[0]].inc(count)
    else:
        parentTree.children[items[0]] = tree(items[0], parentTree, count)
    if len(items) > 1:
        print "sub update"
        print items[1::]
        print parentTree.children[items[0]].getName()
        updateTree(items[1::], parentTree.children[items[0]], count)

# TODO3: create fp-tree based on database
# TODO4: create conditional fp-tree based on fp-tree

root = tree('root', None, 0)
# incorrect: create treeNode for all frequent items and make them as child of 'root'
for trans, count in rawDict.iteritems():
    # print list(trans) # frozenset(['0', '3', '6'])
    orderedItems = []
    for item in trans:
        if item in freqItemsDict.keys():
            orderedItems.append(item)
    print trans
    print "sorted orderedItems :"
    # print sorted(orderedItems)
    print sorted(orderedItems, key=lambda x: orderedFreqItemsBySupport.index(x[0]))
    # updating the tree
    updateTree(sorted(orderedItems, key=lambda x: orderedFreqItemsBySupport.index(x[0])), root, count)        
# for item in orderedFreqItemsBySupport:
#     root.children[item] = tree(item, root, 0)
root.toString("-")

# orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]


