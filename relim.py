#!/usr/bin/env python

from pymining import itemmining, assocrules


data = (('a','b','c','d','e','f','g','h'),
        ('a','f','g'),
        ('b','d','e','f','j'),
        ('a','b','d','i','k'),
        ('a','b','e','g'))

min_sup = 3
min_conf = 0.5

# get frequent itemsets using pymining
relim_input = itemmining.get_relim_input(data)
frequent_itemsets = itemmining.relim(relim_input, min_sup)

# get association rules using pymining
results = assocrules.mine_assoc_rules(frequent_itemsets, min_sup, min_conf)

for key in frequent_itemsets.keys():
	print(str(key)+" : "+str(frequent_itemsets[key]))

for key in results:
	print(str(key))