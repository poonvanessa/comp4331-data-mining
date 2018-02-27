#!/usr/bin/python

import urllib2

data = urllib2.urlopen('https://raw.githubusercontent.com/HKUSTcomp4331/sample-code-data-mining/master/freq_items_dataset.txt').read() # it's a file like object and works just like a file
# print data
data = data.split("\n")
list = []
for line in data: # files are iterable
    # print line + ';'
    items = line.split(" ")
    for item in items:
        if item != "":
            list.append(item)

# list = [ '25', '52', '164', '240', '274', '328', '368', '448', '538', '561', '630', '687', '730', '775', '825', '834' ]
minsup = 100
k = 1 

dict = {}
# generate frequent itemsets of length 1
for i in xrange(0,9):
    dict[str(i)] = 0
# scan through database and count for the support of candidates
for item in list:
    for key, value in dict.iteritems():
        # print key + ' : ' + str(value)
        if key in item:
            dict[key] = value + 1
# removing elements below support threshold 
for key in dict.keys():
    if dict[key] <= minsup :
        del dict[key]



key_list_2 = dict.keys()
dict2 = {}
# generate frequent itemsets of length 2
for key in  key_list_2:
    for key2 in key_list_2:
        dict2[key+key2] = 0
# scan through database and count for the support of candidates
for item in list:
    for key, value in dict2.iteritems():
        # print key + ' : ' + str(value)
        if key in item:
            dict2[key] = value + 1
# removing elements below support threshold 
for key in dict2.keys():
    if dict2[key] <= minsup :
        del dict2[key]


key_list_3 = dict2.keys()
dict3 = {}
# generate frequent itemsets of length 2
for key in  key_list_3:
    for key2 in key_list_3:
        if key[1:] == key2[:-1]:
           dict3[key+key2[-1]] = 0
# scan through database and count for the support of candidates
for item in list:
    for key, value in dict3.iteritems():
        # print key + ' : ' + str(value)
        if key in item:
            dict3[key] = value + 1
# removing elements below support threshold 
for key in dict3.keys():
    if dict3[key] <= minsup :
        del dict3[key]



# printing dict values
for key, value in dict.iteritems():
    print key + ' : ' + str(value)
# printing dict2 values
for key, value in dict2.iteritems():
    print key + ' : ' + str(value)
# printing dict3 values
for key, value in dict3.iteritems():
    print key + ' : ' + str(value)