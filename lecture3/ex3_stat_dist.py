# from numpy.linalg import *
# import numpy as np
# from scipy import *
# from scipy.stats import chi2
# import random
# import matplotlib.pyplot as plt
# import pandas as pd
# import networkx as nx
import pylab, scipy.stats

def statistical_distribution(samples, sets):

	X = pylab.standard_normal((samples, sets))
	s = pylab.sum(X * X, axis=0)

	(n, bins, patches) = pylab.hist(s, bins=100)

	x = pylab.linspace(0, max(s), 100)
	y = scipy.stats.chi2.pdf(x,samples) * sets * pylab.diff(bins)[0]

	pylab.plot(x, y, "y", linewidth=5)
	pylab.show()


	# S = [sum(map(pow, [random.gauss(1, random.random()) for x in range(0,samples)], [2 for x in range(0,samples)] )) for y in range(0,sets)]
	
	# (n bins, patches) = pylab.histogram(S, bins = 100)

	# # plt.bar(np.mean(S), hist, align='center')

	# rv = chi2.pdf(S)
	# x = np.linspace(0, np.minimum(rv.dist.b, 3))
	# h = plt.plot(x, rv.pdf(x))
	
	# plt.plot(chi2.pdf(10, S))
	# # plt.plot(S)
	# plt.show()

	# pdf(S)
	# x = linspace(0.1, 25, 200)
	# plot(x, chi2.pdf(x, S))
	# rv = chi2(S)
	# fig, ax = plt.subplots(1, 1)	
	# ax.plot(x, rv.pdf(x), 'k-', lw=2, label='frozen pdf')


if __name__ == '__main__':
    statistical_distribution(10, 10000)