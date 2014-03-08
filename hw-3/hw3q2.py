#!/usr/bin/python

import scipy as sp
from scipy.sparse import *
import numpy as np
from scipy import *
import random as rnd
from time import time

avg = lambda L: 1.0*sum(L)/len(L)

def readfile(fname):
	for edge in open(fname):
		yield [int(v) for v in edge.split('\t')]

def error(P, R, n):
	IP = sorted(range(len(P)), key = lambda k: P[k])
	# IR = sorted(range(len(R)), key = lambda k: R[k])
	IP.reverse()
	# IR.reverse()
	return 1.0*sum([abs(P[IP[i]] - R[IP[i]]) for i in range(n)])/n

def mc(fname, R, beta = 0.8):
	G = {}
	for T in readfile(fname):
		if T[0] not in G: G[T[0]] = [T[1]]
		else: G[T[0]].append(T[1])
	
	n = len(G)
	# frequency count 
	f = [0 for k in range(n)]
	# simulate random walk 
	# for each vertex 
	for v in G:
		# simulate it R times
		for iter in range(R):
			# walk terminates at each node with prob. 1-beta
			node = v
			while True:
				f[node-1] = f[node-1]+1
				if rnd.uniform(0, 1) > 1-beta: # continue the walk 
					node = G[node][rnd.randint(0, len(G[node])-1)]
				else: # game over 
					break
		# print f
	r = [(1-beta)*f[i]/(n*R) for i in range(n)]
	return r

def pagerank(fname, beta = 0.8):
	row = []
	col = []
	for T in readfile(fname):
		row.append(T[0]-1)
		col.append(T[1]-1)
	n = 100
	row = array(row)
	col = array(col)
	dat = array([1.0 for k in row])
	# convert it to full matrix to simplify our life 
	M = csc_matrix((dat, (row, col)), shape = (n, n) ).todense()
	# make it column stohastic 
	for i in range(n): M[:, i] = M[:, i].dot(1.0/M[:, i].sum())
	# initialize page rank vector 
	r = np.transpose(array([1.0/n for k in range(n)]))
	t = np.transpose(array([(1-beta)/n for k in range(n)]))
	# now do power iteration 
	for i in range(40):
		r = array(t+beta*M.dot(r))
		r = r[0,:]
	return r

# entry point 
if __name__ == '__main__':
	# compute PageRank with Power iteration 
	pr = pagerank('graph.txt', 0.8)
	#T = []
	#for i in range(50):
	#	start = time()
	#	pr = pagerank('graph.txt', 0.8)
	#	T.append(time() - start)
	#print avg(T)
	
	# now run the MC algortihm 
	r1 = mc('graph.txt', 1, 0.8)
	r3 = mc('graph.txt', 3, 0.8)
	r5 = mc('graph.txt', 5, 0.8)
	
	print "*"*3, "R = 1", "*"*3
	print "Top 10: ", error(pr, r1, 10)
	print "Top 30: ", error(pr, r1, 30)
	print "Top 50: ", error(pr, r1, 50)
	print "All   : ", error(pr, r1, len(r1))
	
	print "*"*3, "R = 3", "*"*3
	print "Top 10: ", error(pr, r3, 10) 
	print "Top 30: ", error(pr, r3, 30) 
	print "Top 50: ", error(pr, r3, 50)
	print "All   : ", error(pr, r3, len(r3))
	
	print "*"*3, "R = 5", "*"*3
	print "Top 10: ", error(pr, r5, 10)
	print "Top 30: ", error(pr, r5, 30)
	print "Top 50: ", error(pr, r5, 50)
	print "All   : ", error(pr, r5, len(r5))
