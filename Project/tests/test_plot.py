# import plotly.plotly as py
# from plotly.graph_objs import *
# # Fill in with your personal username and API key
# # or, use this public demo account
# py.sign_in('Python-Demo-Account', 'gwt101uhh0')
# import numpy as np


# y0 = np.random.randn(50)
# y1 = np.random.randn(50)+1

# trace1 = Box(
#     y=y0
# )
# trace2 = Box(
#     y=y1
# )
# data = Data([trace1, trace2])
# plot_url = py.plot(data, filename='basic-box-plot')


from pylab import *
from scipy.io import loadmat

# NYCdiseases = loadmat('NYCDiseases.mat') # it's a matlab file

# multiple box plots on one figure
# Chickenpox cases by month
figure(1)
# NYCdiseases['chickenPox'] is a matrix 
# with 30 rows (1 per year) and 12 columns (1 per month)

numbers = [[3,2,3,2,3], [5,2,3,4,5], [1,2,3,4,5], [1,2,3,4,5], [1,2,3,4,5], [1,2,3,4,5], [1,2,3,4,5], [1,2,3,4,5]]
boxplot(numbers)

labels = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
xticks(range(1,13),labels, rotation=15)
xlabel('Month')
ylabel('Chickenpox cases')
title('Chickenpox cases in NYC 1931-1971')
show()