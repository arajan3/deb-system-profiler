import pandas as pd
from sklearn import preprocessing
import numpy as np
import matplotlib.pyplot as plt

# Choose how many bins you want here
num_bins = 100

data = pd.read_csv("deb-results.csv", header=None)

x = data[1].values
x_scaled = preprocessing.MinMaxScaler().fit_transform(x.reshape(-1,1))

counts, bin_edges = np.histogram(x_scaled, bins=num_bins, normed=True)
# Now find the cdf
cdf = np.cumsum(counts)
# And finally plot the cdf
plt.plot(cdf, bin_edges[1:])
plt.suptitle('CDF of deb-package scores', fontsize=20)
plt.xlabel('% of scores', fontsize=14)
plt.ylabel('CDF', fontsize=14)
plt.savefig('deb-results.cdf.jpg')
plt.clf()

data = pd.read_csv("file-results.csv", header=None)
x = data[1].values
x_scaled = preprocessing.MinMaxScaler().fit_transform(x.reshape(-1,1))

counts, bin_edges = np.histogram(x_scaled, bins=num_bins, normed=True)
# Now find the cdf
cdf = np.cumsum(counts)
# And finally plot the cdf
plt.plot(cdf, bin_edges[1:])
plt.suptitle('CDF of file scores', fontsize=20)
plt.xlabel('% of scores', fontsize=14)
plt.ylabel('CDF', fontsize=14)
plt.savefig('file-results.cdf.jpg')
plt.clf()