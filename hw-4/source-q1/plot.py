#!/usr/bin/python

import os, sys, time
import numpy as np
from matplotlib import pyplot

if __name__ == '__main__':
	# Batch gradient descent 
	Y_bgd = []
	X = []
	k = 0
	for ln in open('hw4q1-bgd-a.txt').read().split('\n'):
		if ln[:8] == 'crr_cost':
			X.append(k)
			Y_bgd.append(float(ln.split()[1]))
			k = k+1
	pyplot.plot(X, Y_bgd)
	pyplot.show()
	print "X = ", X
	print "Y = ", Y_bgd
	
	# Stohastic gradient descent 
	k = 0
	X = []
	Y_sgd = []
	for ln in open('hw4q1-sgd-a.txt').read().split('\n'):
		if ln[:8] == 'crr_cost':
			X.append(k)
			Y_sgd.append(float(ln.split()[1]))
			k = k+1
	for i in range(len(Y_sgd) - len(Y_bgd)): Y_bgd.append(Y_bgd[-1])
	pyplot.plot(X, Y_sgd, X, Y_bgd)
	pyplot.show()
	print "X = ", X
	print "Y = ", Y_sgd
	
	# Mini Batch Gradient Descent 
	k = 0
	#X = []
	Y_mbgd = []
	for ln in open('mini-bgd-a.txt').read().split('\n'):
		if ln[:8] == 'crr_cost':
			#X.append(k)
			Y_mbgd.append(float(ln.split()[1]))
			k = k+1
	for i in range(len(Y_sgd) - len(Y_mbgd)): Y_mbgd.append(Y_mbgd[-1])
	pyplot.plot(X, Y_sgd, X, Y_bgd, X, Y_mbgd)
	pyplot.show()
	print "X = ", X
	print "Y = ", Y_mbgd
