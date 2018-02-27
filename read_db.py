#!/usr/bin/python
import urllib2

data = urllib2.urlopen('https://raw.githubusercontent.com/HKUSTcomp4331/sample-code-data-mining/master/freq_items_dataset.txt').read(200) # it's a file like object and works just like a file
data = data.split("\n")
list = []
for line in data: # files are iterable
    print line + ';'
    items = line.split(" ")
    for item in items:
        if item != "":
            list.append(item)

print list


