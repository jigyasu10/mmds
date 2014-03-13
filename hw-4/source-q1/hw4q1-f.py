#!/usr/bin/python

import os, sys, time
import numpy as np
from numpy import linalg
import random as rnd
from matplotlib import pyplot

# derivative of hinge by wj; here, i is index of the training example 
def hinge(X, Y, w, b, j, i, C):
	return C*(0 if Y[i]*(np.dot(X[i], w)+b) >= 1 else -X[i][j]*Y[i])

# compute cost function --- iterates over the whole dataset
def f(X, Y, w, b, C):
	return linalg.norm(w)**2/2 + C*sum([max(0, 1.0-Y[i]*(np.dot(w, X[i])+b)) for i in range(len(X))]) 

# derivative of f by b 
def grad_b(X, Y, w, b, i, C):
	return C*(0 if Y[i]*(np.dot(X[i], w)+b) >= 1 else -Y[i]) # C=100

# stohastic gradient descent 
def sgd(X, Y, w, b, ni = 0.0001, eps = 0.001, C = 100):
	I = range(len(X))
	rnd.shuffle(I)
	X = [X[i] for i in I]
	Y = [Y[i] for i in I]
	i, k = 1, 0
	n = len(X)
	crr_f = prev_f = f(X, Y, w, b, C)
	#print "crr_cost: ", crr_f
	delta_cost = 0.0
	while True:
		tw = list(w)
		# update 
		for j in range(len(X[0])):
			tw[j] = w[j] - ni*(w[j] + hinge(X, Y, w, b, j, i, C)) # derivative of hinge by w[j] 
		b = b - ni*grad_b(X, Y, w, b, i, C)
		w = list(tw)
		i = ((i+1) % n)
		k = k+1
		crr_f = f(X, Y, w, b, C)
		#print "crr_cost: ", crr_f
		delta_cost = 0.5*delta_cost + 0.5*(abs(prev_f - crr_f))*100/(prev_f)
		if k%500 == 0: print "k=", k
		#print "delta_cost: ", delta_cost
		#print "-"*80
		if delta_cost < eps:
			#print "[DONE] Converged after", k, "steps"
			break
		prev_f = crr_f
	print "Final f=", crr_f, "after", k, "steps"
	return (w, b)

def load_ftr(fname):
	return [[int(el) for el in line.split(',')] for line in open(fname).read().split()]

def load_trg(fname):
	return [int(el) for el in open(fname).read().split()]

def est_err(X, Y, w, b):
	n = len(X)
	miss = 0
	for i in range(n):
		if Y[i]*(np.dot(X[i], w)+b) <= 0: miss = miss+1
	print "[DEBUG] Misclassified", miss, "out of", n
	return 1.0*miss/n

# entry point 
if __name__ == '__main__':
	Cs = [1, 10, 50, 100, 200, 300, 400, 500]
	# train data 
	X = load_ftr('features.train.txt')
	Y = load_trg('target.train.txt')
	# test data 
	X_test = load_ftr('features.test.txt')
	Y_test = load_trg('target.test.txt')
	E = []
	for C in Cs:
		X = load_ftr('features.train.txt')
		Y = load_trg('target.train.txt')
		w = [0 for x in range(len(X[0]))]
		b = 0
		(w, b) = sgd(X, Y, w, b, 0.0001, 0.001, C)
		print "w=", w 
		print "b=", b
		E.append(est_err(X_test, Y_test, w, b))
		print "For C=", C, "the percent error equals", E[-1]
		print "-" * 80
	print "E=", E
	pyplot.plot(Cs, E)
	pyplot.show()
