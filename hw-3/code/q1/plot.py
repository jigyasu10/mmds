import matplotlib.pyplot as plt 
"""
X = []
Y = []
for line in open('tmp.dat'):
	T = [float(x) for x in line.split(":")]
	X.append(T[0])
	Y.append(T[1])

print X
print Y
plt.plot(X, Y)
plt.show()
"""

X = []
Y = []
#for line in open('nonreg.plot'):
#for line in open('reg.plot'):
for line in open('tmp.dat'):
	T = [float(x) for x in line.split(":")]
	X.append(T[0])
	Y.append(T[1])

# X = X[:10]
# plt.plot(X, Y[:10], 'g') # nonregularized 
# plt.plot(X, Y[10:], 'b') # regularized 
plt.plot(X, Y)
plt.show()
