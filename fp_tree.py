#!/usr/bin/python
class tree:
    def __init__(self, itemName, parent, count):
        self.itemName = itemName
        self.parent = parent
        self.count = count
        self.children = {}
        self.nodeLink = None

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
    def printNodeLinked(self):
        result = ""
        temp = self
        while temp!=None:
            result = result + " - " +temp.itemName + ":"+str(temp.count)+"; "
            temp = temp.nodeLink
        print result
    def inc(self,counter):
        self.count = self.count + counter

# accept a list of frequent items and update the fp-tree
# items: char list, parentTree: tree, count: int
def updateTree(items, parentTree, count, headerDict):
    # print "updateTree is called - "+parentTree.getName()+" : "+str(count)
    # print items
    
    if items[0] in parentTree.children: 
        parentTree.children[items[0]].inc(count)
    else:
        parentTree.children[items[0]] = tree(items[0], parentTree, count)
        if items[0] in headerDict:
            # print "updateHeader - "+items[0]
            updateHeader(headerDict[items[0]],parentTree.children[items[0]])
        else:
            # print "addHeader - "+items[0]
            headerDict[items[0]] = parentTree.children[items[0]]
    if len(items) > 1:
        # print "sub update"
        # print items[1::]
        # print parentTree.children[items[0]].getName()
        updateTree(items[1::], parentTree.children[items[0]], count, headerDict)
    # if parentTree.itemName == 'root':
        # print "------------------------------------------------"

# Dict: element of headerDict, treeNode: new tree node to be updated/linked
def updateHeader(Dict, treeNode):
    if Dict.nodeLink == None:
        Dict.nodeLink = treeNode
        # print "Dict equals to None"
    else:
        while (Dict.nodeLink!=None):
            Dict= Dict.nodeLink
        Dict.nodeLink = treeNode

    # print out content of headerDict
    for key, node in headerDict.iteritems():
        print "key : "+key
        node.printNodeLinked()

# construct fp-tree
# rawDict: { tuple(transaction): counter, ...}, freqItemsDict: {char: support, ...} only contains those above threshold, orderedFreqItemsBySupport: list for sorting
# root: root treeNode, headerDict: Dictionay to store headerLinkedNode
def constructTree(rawDict, freqItemsDict, orderedFreqItemsBySupport, root, headerDict):
    for trans, count in rawDict.iteritems():
        # print list(trans) # frozenset(['0', '3', '6'])
        orderedItems = []
        for item in trans:
            if item in freqItemsDict.keys():
                orderedItems.append(item)
        # print trans
        # print "sorted orderedItems :"
        # print sorted(orderedItems)
        # print sorted(orderedItems, key=lambda x: orderedFreqItemsBySupport.index(x[0]))
        # updating the tree
        updateTree(sorted(orderedItems, key=lambda x: orderedFreqItemsBySupport.index(x[0])), root, count, headerDict) 
    return root, headerDict

data = [ '25', '52', '164', '240', '274', '328', '368', '448', '538', '561', '630', '687', '730', '775', '825', '834' ]

minsup = 5
freqItemsDict = {}  # {'3': 6, '2': 6, '5': 6, '4': 6, '8': 7}  only those above the threshold
rawDict = {}    # { frozenset(['2','5']): 2, frozenset(['1','4', '6']): 1 ... }
headerDict = {}

# prepare data
for trans in data:
    print list(trans)
    # print "trans" + list(trans) + str(type(trans))
    rawDict[tuple(trans)] = rawDict.get(tuple(trans), 0) + 1
    for item in trans:
        freqItemsDict[item] = freqItemsDict.get(item, 0) + 1
print rawDict   #{('5', '6', '1'): 1, ('7', '7', '5'): 1, ('5', '3', '8'): 1, ('6', '3', '0'): 1, ('7', '3', '0'): 1, ('2', '4', '0'): 1, ('8', '3', '4'): 1, ('3', '2', '8'): 1, ('5', '2'): 1, ('2', '7', '4'): 1, ('3', '6', '8'): 1, ('4', '4', '8'): 1, ('6', '8', '7'): 1, ('2', '5'): 1, ('8', '2', '5'): 1, ('1', '6', '4'): 1}
# filter out candidate of length 1 which are below threshold
for key in freqItemsDict.keys():
    if freqItemsDict[key] <= minsup :
        del freqItemsDict[key]    


orderedFreqItemsBySupport = [v[0] for v in sorted(sorted(freqItemsDict.items(), key=lambda q:q[0], reverse=False), key=lambda p: p[1], reverse=True)]
print orderedFreqItemsBySupport # a list of sorted freqItemsDict

root = tree('root', None, 0)
root, headerDict = constructTree(rawDict, freqItemsDict, orderedFreqItemsBySupport, root, headerDict)
root.toString("-")

# print headerDict
for key, node in headerDict.iteritems():
    print "key : "+key
    node.printNodeLinked()

print "start: scanning headerDict"
condTreeDict = {}
# scan the node from bottom to top and print out path from leave to root
for leaveNodeKey, leaveNode in headerDict.iteritems():
    localD = {}
    localRawD = {}
    localHeader = {}
    # leaveNode = headerDict['5']

    # treeNode.toString("-")
    while (leaveNode!=None):
        leave = leaveNode
        tempList = []
        while (leave.parent!=None):
            localD[leave.itemName] = localD.get(leave.itemName,0) + leaveNode.count
            tempList.append(leave.itemName)
            print leave.itemName + " : "+ str(localD.get(leave.itemName,0))
            leave = leave.parent
        localRawD[tuple(tempList)] = leaveNode.count
        leaveNode = leaveNode.nodeLink
    # print localD    #{'8': 2, '3': 1, '2': 3, '5': 6}

    # print localRawD     #{('5', '2', '8'): 1, ('5', '2'): 2, ('5', '3', '8'): 1, ('5',): 2}
    for key in localD.keys():
        if localD[key] < 2:
            del localD[key]
    #print localD   #{'8': 2, '2': 3, '5': 6}
    localFrequentList = [v[0] for v in sorted(sorted(localD.items(), key=lambda q:q[0], reverse=False), key=lambda p: p[1], reverse=True)]
    # print localFrequentList  #['5', '2', '8']

    localRoot = tree('root', None, 0)

    condTreeDict[leaveNodeKey], localHeader = constructTree(localRawD, localD, localFrequentList, localRoot, localHeader)

    # localTreeNode.toString("-")

for treeKey, condTree in condTreeDict.iteritems():
    print treeKey +" : "
    condTree.toString("-")

# for trans, count in localRawD.iteritems():
#     # print list(trans) # frozenset(['0', '3', '6'])
#     orderedItems = []
#     for item in trans:
#         if item in localFrequentList:
#             orderedItems.append(item)
#     print trans
#     print "sorted orderedItems :"
#     # print sorted(orderedItems)
#     print sorted(orderedItems, key=lambda x: localFrequentList.index(x[0]))
#     # updating the tree
#     updateTree(sorted(orderedItems, key=lambda x: localFrequentList.index(x[0])), localRoot, count, headerDict)
# localRoot.toString("-")


#TODO1: turn localD into orderedlist and then construct a fp-tree where leaveNode is root
