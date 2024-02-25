import numpy as np
import seaborn as sns 
import matplotlib.pyplot as plt
from numpy import genfromtxt

heat_data = genfromtxt('ha.csv', delimiter=',')
ax = sns.heatmap(heat_data, linewidths=0, cmap='YlGnBu')

plt.show()