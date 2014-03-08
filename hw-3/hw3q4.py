#!/usr/bin/python

from time import time
import matplotlib.pyplot as plt
import math

error = lambda P, R, I, n: 1.0*sum([abs(P[I[i]] - R[I[i]]) for i in range(n)])/n
avg = lambda L: 1.0*sum(L)/len(L)

# we count each edge twice, 2|E(G)| = sum_v deg(v), so we need to factor out 2 
density = lambda S: avg(S.values())/2 if len(S) > 0 else 0

def readfile(fname):
	for edge in open(fname):
		yield [int(v) for v in edge.split()]

# basic version of the algorithm 
def algo(fname, eps):
	S = {}
	T = {}
	for e in readfile(fname):
		# print e
		S[e[0]] = 1 if e[0] not in S else S[e[0]]+1
		S[e[1]] = 1 if e[1] not in S else S[e[1]]+1
	dS = density(S)
	print dS
	i = 1
	plot_rhos = [dS]
	plot_edgs = [sum(S.values())/2]
	plot_sizs = [len(S)]
	plot_X = [i]
	while len(S) > 0:
		tS = {}
		for v in S:
			if S[v] > 2*(1+eps)*dS: tS[v] = 0
		for e in readfile(fname): # compute S \ A(S) 
			if e[0] in tS and e[1] in tS:
				tS[e[0]] = tS[e[0]]+1
				tS[e[1]] = tS[e[1]]+1
		S = dict(tS)
		dS = density(tS)
		if dS > density(T): T = dict(tS)
		i = i+1
		plot_rhos.append(dS)
		plot_edgs.append(sum(S.values())/2 if len(S) > 0 else 0)
		plot_sizs.append(len(S))
		plot_X.append(i)
		print "Current density: ", dS
		print "|S|=", len(S), "|T|=", len(T)
		print "-"*80
	# print T
	print density(T)
	print "Done"
	
	# print "rhos=", plot_rhos
	# print "edgs=", plot_edgs
	# print "sizs=", plot_sizs
	
	plt.plot(plot_X, plot_rhos, 'r')
	plt.draw()
	
	plt.figure()
	plt.plot(plot_X, plot_edgs, 'g')
	plt.draw()
	
	plt.figure()
	plt.plot(plot_X, plot_sizs, 'b')
	plt.draw()
	
	plt.show()
	
	return i

# stops after it finds 20 communities 
# NOTE: Due to time constraints the code is not efficient
def multiple_components(fname, eps = 0.05):
	D = set()
	plot_rhos = []
	plot_sizs = []
	plot_edgs = []
	plot_X = []
	for i in range(1, 21):
		start = time()
		S = {} 
		T = {} 
		for e in readfile(fname):
			if e[0] not in D and e[1] not in D:
				S[e[0]] = 1 if e[0] not in S else S[e[0]]+1
				S[e[1]] = 1 if e[1] not in S else S[e[1]]+1
		dS = density(S)
		while len(S) > 0:
			tS = {}
			for v in S:
				if S[v] > 2*(1+eps)*dS: tS[v] = 0
			for e in readfile(fname): # compute S \ A(S) 
				if e[0] in tS and e[1] in tS:
					tS[e[0]] = tS[e[0]]+1
					tS[e[1]] = tS[e[1]]+1
			S = dict(tS)
			dS = density(tS)
			if dS > density(T): T = dict(tS)
		plot_rhos.append(density(T))
		plot_edgs.append(sum(T.values())/2 if len(T) > 0 else 0)
		plot_sizs.append(len(T))
		plot_X.append(i)
		for v in T: D.add(v)
		print "Current density: ", density(T)
		print "|T|=", len(T)
		print "|E[T]|=", sum(T.values())/2
		print "Community found in ", time()-start, "seconds"
		print "-"*80
	
	plt.plot(plot_X, plot_rhos, 'r')
	plt.draw()
	
	plt.figure()
	plt.plot(plot_X, plot_edgs, 'g')
	plt.draw()
	
	plt.figure()
	plt.plot(plot_X, plot_sizs, 'b')
	plt.draw()
	
	plt.show()

# entry point 
if __name__ == '__main__':
	# algo('livejournal-undirected-small.txt', 0.01)
	"""
	n = 499923
	X = [0.1, 0.5, 1.0, 2.0]
	for eps in X:
		start = time()
		# algo returns the number of steps 
		Y.append(algo('livejournal-undirected.txt', eps))
		print "time: ", time()-start, "seconds"
	print "X=", X
	print "Y=", Y
	plt.plot(X, Y)
	plt.plot(X, [math.log(n, 1+x) for x in X])
	plt.show()
	""" 
	
	# print algo('livejournal-undirected.txt', 0.05)
	
	multiple_components('livejournal-undirected.txt', 0.05)
	