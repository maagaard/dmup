from pylab import *
from scipy.stats import chi2

def test():
	x = linspace(0.1, 25, 200)
	for dof in [1, 2, 3, 5, 10, 50]:
		plot(x, chi2.pdf(x, dof))
