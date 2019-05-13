import pandas as pd
from sklearn import preprocessing
import numpy as np
import matplotlib.pyplot as plt

# Choose how many bins you want here
num_bins = 100

data = pd.read_csv("deb-results.csv", header=None)

x = data[1].values
x_scaled = preprocessing.MinMaxScaler().fit_transform(x.reshape(-1,1))

plt.hist(x_scaled, normed=True, bins=num_bins)
plt.suptitle('Histogram of deb-package scores', fontsize=20)
plt.xlabel('Ranges of scores', fontsize=14)
plt.ylabel('Histogram', fontsize=14)
plt.savefig('deb-results.hist.jpg')
plt.clf()

data = pd.read_csv("file-results.csv", header=None)
x = data[1].values
x_scaled = preprocessing.MinMaxScaler().fit_transform(x.reshape(-1,1))

plt.hist(x_scaled, normed=True, bins=num_bins)
plt.suptitle('Histogram of file scores', fontsize=20)
plt.xlabel('Ranges of scores', fontsize=14)
plt.ylabel('Histogram', fontsize=14)
plt.savefig('file-results.hist.jpg')
plt.clf()