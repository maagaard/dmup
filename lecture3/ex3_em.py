from numpy.linalg import *
import numpy as np
from scipy import *
from scipy.stats import chi2
import random
import matplotlib.pyplot as plt
import pandas as pd

def matrixrank(A, tol=None):
	"""Compute rank"""

	U, s, V = svd(A, full_matrices=True)
	return len(filter(lambda x: x >= tol, s))


def stat(samples, sets):


	S = [sum(map(pow, [random.gauss(1, random.random()) for x in range(0,samples)], [2 for x in range(0,samples)] )) for y in range(0,sets)]
	hist, bins = np.histogram(S, bins = 100)

	# plt.bar(np.mean(S), hist, align='center')

	rv = chi2.pdf(S)
	x = np.linspace(0, np.minimum(rv.dist.b, 3))
	h = plt.plot(x, rv.pdf(x))
	
	# plt.plot(chi2.pdf(10, S))
	# # plt.plot(S)
	# plt.show()

	# pdf(S)
	# x = linspace(0.1, 25, 200)
	# plot(x, chi2.pdf(x, S))
	# rv = chi2(S)
	# fig, ax = plt.subplots(1, 1)	
	# ax.plot(x, rv.pdf(x), 'k-', lw=2, label='frozen pdf')
def lol():
	x = np.arange(0, 5, 0.1);
	y = np.sin(x)
	plt.plot(x, y)
	plt.show()


# stat(10, 10000)


def coauth():
	authors = pd.read_csv('coauthors.csv', index_col=False, sep='\t')
	print authors.shape, authors.ndim


coauth()