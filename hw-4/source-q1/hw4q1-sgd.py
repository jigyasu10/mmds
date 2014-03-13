#!/usr/bin/python

import os, sys, time
import numpy as np
from numpy import linalg
import random as rnd
import timeit

# derivative of hinge by wj; here, i is index of the training example 
def hinge(X, Y, w, b, j, i):
	return 100*(0 if Y[i]*(np.dot(X[i], w)+b) >= 1 else -X[i][j]*Y[i]) # C=100

# compute cost function --- iterates over the whole dataset
def f(X, Y, w, b):
	return linalg.norm(w)**2/2 + 100*sum([max(0, 1.0-Y[i]*(np.dot(w, X[i])+b)) for i in range(len(X))]) # C=100

# derivative of f by b 
def grad_b(X, Y, w, b, i):
	return 100*(0 if Y[i]*(np.dot(X[i], w)+b) >= 1 else -Y[i]) # C=100

# stohastic gradient descent 
def sgd(X, Y, w, b, ni = 0.0001, eps = 0.001):
	I = range(len(X))
	rnd.shuffle(I)
	X = [X[i] for i in I]
	Y = [Y[i] for i in I]
	i, k = 1, 0
	n = len(X)
	crr_f = prev_f = f(X, Y, w, b)
	print "crr_cost: ", crr_f
	delta_cost = 0.0
	while True:
		tw = list(w)
		# update 
		for j in range(len(X[0])):
			tw[j] = w[j] - ni*(w[j] + hinge(X, Y, w, b, j, i)) # derivative of hinge by w[j] 
		b = b - ni*grad_b(X, Y, w, b, i)
		w = list(tw)
		i = (i % n) + 1
		k = k+1
		crr_f = f(X, Y, w, b)
		print "crr_cost: ", crr_f
		delta_cost = 0.5*delta_cost + 0.5*(abs(prev_f - crr_f))*100/(prev_f)
		print "k=", k
		print "delta_cost: ", delta_cost
		print "-"*80
		if delta_cost < eps:
			print "[DONE] Converged after", k, "steps"
			break
		prev_f = crr_f
	return (w, b)

def load_train(fname):
	return [[int(el) for el in line.split(',')] for line in open(fname).read().split()]

def load_test(fname):
	return [int(el) for el in open(fname).read().split()]

# entry point 
if __name__ == '__main__':
	#X = load_train('features.txt')
	#Y = load_test('target.txt')
	#w = [0 for x in range(len(X[0]))]
	#b = 0
	#(w, b) = sgd(X, Y, w, b)
	s = "	X = load_train('features.txt')\n\
	Y = load_test('target.txt')\n\
	w = [0 for x in range(len(X[0]))]\n\
	b = 0\n\
	(w, b) = sgd(X, Y, w, b)"
	print(timeit.timeit(s, setup="from __main__ import *", number=1))
