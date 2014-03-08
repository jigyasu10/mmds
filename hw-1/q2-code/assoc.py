#!/usr/bin/python 
#
# naive implementation of first 3 phases of apriori as described in the MMDS textbook 
# DISCLAIMER: I wrote this on a long train ride, so the code is very ugly. 
#

import sys

SUPPORT = 100 

iname = {} # inverse 
name = {} # maps names to integers 
single_counts = [0] # singleton counts 

freq_table = [] # frequent singletons 
pair_counts = [] # pair counts 

# get_idx = lambda i, j, n: (i-1)*n-i*(i-1)/2+j-i
get_idx = lambda i, j, n: i*n-i*(i+1)/2+j-i

# simple data structure that holds top k rules, i.e. the ones with the highest confidences 
class Rules:
	def __init__(self, c = 0.0, k = 5):
		self.c = c
		self.k = k
		self.L = []
		#self.cfds = []
	# add rule I -> j, with conf(I -> j) = c 
	def add(self, I, j, c):
		# self.cfds.append(c)
		if len(self.L) == 0 or c >= max([x[2] for x in self.L]):
			self.L.insert(0, (I, j, c))
		else:
			i = 0
			while i < len(self.L):
				if self.L[i][2] <= c:
					self.L.insert(i, (I, j, c))
					break
				i += 1
		if self.k < len(self.L): self.L = self.L[:-1]
		

## the rest of the HW1Q2 solution 

def indices(idx, m):
	i = 0
	s = 0
	while idx > s:
		i += 1
		s += (m-i)
	j = idx-(s-m+i+1)+i
	return (i-1, j)

def apriori(fname):
	# 1st pass 
	N = 1
	for basket in open(fname):
		for item in set([item for item in basket.split(' ') if len(item) > 5]):
			item = item.strip()
			if item not in name:
				name[item] = N
				iname[N] = item
				single_counts.append(0)
				N += 1
			single_counts[name[item]] += 1
	freq_table = [0 for k in single_counts]
	m = 1
	# renumber frequent items 
	for item in [item for item in name.values() if single_counts[item] >= SUPPORT]:
		freq_table[item] = m
		m += 1
	
	print "Number of frequent items:", m-1
	
	# triangular matrix 
	pair_counts = [0 for k in range(m*(m+1)/2)]
	# 2nd pass 
	
	print "Generating all pairs"
	for basket in open(fname):
		T = [item.strip() for item in set(basket.split(' ')) if len(item) > 5 and single_counts[name[item]] >= SUPPORT] # frequent items from this basket 
		for (item1, item2) in [(name[item1], name[item2]) for item1 in T for item2 in T if freq_table[name[item1]] < freq_table[name[item2]]]:
			pair_counts[get_idx(freq_table[item1], freq_table[item2], m)] += 1
	
	# (idx/m, idx-m*(idx/m)) 
	# frequent pairs 
	freq_pairs = [idx for idx in range(len(pair_counts)) if pair_counts[idx] >= SUPPORT]
	r_2 = Rules(0.0, 10) # top 5 rules 
	# confidence = [0 for k in pair_counts]
	print "Computing confidence for all possible rules"
	for idx in freq_pairs:
		(i, j) = indices(idx, m)
		i = [x for x in range(len(freq_table)) if freq_table[x] == i][0]
		j = [x for x in range(len(freq_table)) if freq_table[x] == j][0]
		confidence = 1.0*pair_counts[idx]/single_counts[i]
		r_2.add(iname[i], iname[j], confidence)
		confidence = 1.0*pair_counts[idx]/single_counts[j]
		r_2.add(iname[j], iname[i], confidence)
	
	print "Number of frequent pairs:", len(freq_pairs)
	print "Rules (first 10) generated itemsets of size 2:"
	for rule in r_2.L: print rule 
	
	# r_2.cfds.sort()
	# print r_2.cfds[-10:]
	
	# 3rd pass 
	print "Generating all triplets"
	triple_counts = {}
	for basket in open(fname):
		T = [item.strip() for item in set(basket.split(' ')) if len(item) > 5 and single_counts[name[item]] >= SUPPORT] # frequent items from this basket 
		for (item1, item2, item3) in [(name[item1], name[item2], name[item3]) for item1 in T for item2 in T for item3 in T if freq_table[name[item1]] < freq_table[name[item2]] and freq_table[name[item2]] < freq_table[name[item3]] and get_idx(freq_table[name[item1]], freq_table[name[item2]], m) in freq_pairs and get_idx(freq_table[name[item1]], freq_table[name[item3]], m) in freq_pairs and get_idx(freq_table[name[item2]], freq_table[name[item3]], m) in freq_pairs]:
					triple_counts[(item1, item2, item3)] = 1+triple_counts[(item1,item2, item3)] if (item1,item2, item3) in triple_counts else 1
	
	freq_triplets = [idx for idx in triple_counts if triple_counts[idx] >= SUPPORT]
	r_3 = Rules(0.0, 30)
	print "Computing confidence for all possible rules"
	for (i, j, k) in freq_triplets:
		idx = (i, j, k)
		r_3.add([iname[i], iname[j]], iname[k], 1.0*triple_counts[idx]/pair_counts[get_idx(freq_table[i], freq_table[j], m)])
		r_3.add([iname[i], iname[k]], iname[j], 1.0*triple_counts[idx]/pair_counts[get_idx(freq_table[i], freq_table[k], m)])
		r_3.add([iname[j], iname[k]], iname[i], 1.0*triple_counts[idx]/pair_counts[get_idx(freq_table[j], freq_table[k], m)])
	print "Rules (first 30) generated from itemsets of size 3:"
	for rule in r_3.L: print rule 
	
def idx_test():
	m = 10
	for i in range(10):
		for j in range(i+1, 10):
			idx = get_idx(i, j, 10)
			#print i, j, " -> ", idx
			print i, j, "->", idx, " -> ", indices(idx, m)

# entry point 
if __name__ == "__main__":
	# idx_test()
	fname = sys.argv[1] if len(sys.argv) > 1 else 'browsing.txt'
	apriori(fname) 
