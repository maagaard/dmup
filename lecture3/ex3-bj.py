from numpy.linalg import svd
from random import gauss
from math import sqrt
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chi2
import pandas as pd

def matrixrank(A, tol=None):
    U, s, V = svd(A)
    return len(filter(lambda x: x >= tol , s))
    
def gauss_thing(samples, sets):
    return [sum(map(lambda x: x ** 2, [gauss(1, 0.5) for x in xrange(samples)])) for x in xrange(sets)]

def plot_gauss_thing():
    S = gauss_thing(10, 10000)
    mu, sigma = 100, 15
    x = mu + sigma * np.random.randn(10000)
    hist, bins = np.histogram(S, bins = 100)
    #width = 0.7 * (bins[1] - bins[0])
    width = 1 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.bar(center, hist, align='center', width=width)
    plt.show()
