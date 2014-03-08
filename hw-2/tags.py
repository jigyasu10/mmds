#!/usr/bin/python

import operator

dist = lambda x, c: sum([(x[i]-c[i])**2 for i in range(len(x))])

# d is a document; c is a set of centroids 
def tags(d, c):
	v = open('hw2-q4/vocab.txt').read().split('\n')
	dc = 0
	# find cluster of the document d 
	for k in c: dc = k if dist(d, c[k]) < dist(d, c[dc]) else dc
	# python 2.6 doesn't support dict comprehension  
	t = {}
	for i in range(len(d)): t[i] = d[i]
	t = sorted(t.iteritems(), key=operator.itemgetter(1))
	t.reverse()
	print [v[t[i][0]] for i in range(11)]

# entry point 
if __name__ == '__main__':
	# load documents 
	T = open('hw2-q4/data.txt').read().split('\n')
	X = []
	for t in T: X.append([float(el) for el in t.split()])
	# load the clusters that we got after 20 iterations
	# when initialized with c1.txt 
	T = open('c-19/part-r-00000').read().split('\n')
	C = {}
	i = 0
	for t in T[:-1]:
		if t[:4] != 'cost':
			C[i] = ([float(el) for el in t.split('\t')[1].split()])
			i = i+1
	# compute the tags 
	tags(X[2], C)
