import sys
from scipy import stats
import scipy
import random
from pydoc import help
import os
import csv
import re



#scipy.stats.ttest_ind
#scipy.stats.zscore
#statsmodels.sandbox.stats.multicomp.multipletests

rootdir = "/Users/mleming/Desktop/LFP"
p_dir = os.path.join(rootdir, "Pearson_files")

def transmute(M):
	return [list(i) for i in zip(*M)]

# Returns the mean weight of edges per node in a matrix, for each matrix in a
# set of matrices
def get_mean_connectivity(NNs):
	mNN = []
	for i in range(len(NNs)):
		mNN.append(scipy.mean(NNs[i]))
	return mNN

# Returns the mean weight of edges per node in a matrix
def correlational_covariates(NNs,covs):
	mNN = get_mean_connectivity(NNs)
	p_vals = []
	for i in range(len(covs)):
		(r,p) = scipy.stats.pearsonr(mNN,covs[i])
		p_vals.append(p)
	return p_vals

# Converts a NxN 2D array into 1D array with N^2 elements
def flatten_NN(NN):
	flat_NN = [];
	for i in range(len(NN)):
		for j in range(len(NN[i])):
			flat_NN.append(NN[i][j])
	return flat_NN;

# Plot a histogram of the values in a 2D matrix
def plot_histogram(NN):
	import numpy as np
	import matplotlib.mlab as mlab
	import matplotlib.pyplot as plt

	mu, sigma = 100, 15
	n, bins, patches = plt.hist(flatten_NN(NN), 50, normed=1, facecolor='green', alpha=0.75)
	plt.xlabel('Smarts')
	plt.ylabel('Probability')
	plt.grid(True)
	plt.show()

# Encapsulation for the scatterplot method
def scatter(Y,X = []):
	import numpy as np
	import matplotlib.mlab as mlab
	import matplotlib.pyplot as plt
	if len(X) == 0:
		X = range(len(X))

	plt.scatter(X,Y, s=75, alpha=.5)

	plt.xlabel('X values')
	plt.ylabel('Y values')
	plt.title(r'Plot')
	plt.grid(True)
	plt.show()	

# Reads in all of the CSV files in a given folder into one matrix
def read_in_NNs(NNs_dir):
	NN = []
	for subdir, dirs, files in os.walk(NNs_dir):
		for file in files:
			#print os.path.join(subdir, file)
			NN.append([])
			with open(os.path.join(subdir, file), 'rb') as csvfile:
				spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
				for row in spamreader:
					NN[-1].append([float(x) for x in row])
	return NN

# Reads in the nubers of a CSV file
def read_in_covs_csv(covs_file):
	covs = []
	with open(covs_file, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		t = True
		for row in spamreader:
			if t:
				t = False
			else:
				covs.append([float(x) for x in row])
	return covs

# Extracts all numbers from a string and returns them as floating point
def extract_data(s):
	pattern = re.compile("[\-0-9\.]+") # Catches everything with a -,0-9, or .
	p = pattern.findall(s) # Find everything with this pattern
	return [float(x) for x in p] #Convert from strings to floats

# Reads in numbers of a file using regexes
def read_in_covs_regex(covs_file):
	with open(covs_file, 'rb') as csvfile:
		spamreader = csvfile.readlines()
		for row in spamreader:
			print row
			r = extract_data(row)
			if len(r) > 0:
				covs.append(r)

# Returns the p-values for the correlations between the mean connectivity
# between each matrix in a set of matrices
def ttest_square(NNs):
	square = []
	for x in range(len(NNs)):
		square.append([])
		for y in range(len(NNs)):
			(r,p) = scipy.stats.ttest_ind(get_mean_connectivity(NNs[x]),get_mean_connectivity(NNs[y]))
			square[-1].append(p)
	return square

covs = read_in_covs_csv(os.path.join(rootdir, "covs.csv"))

NNs= read_in_NNs(p_dir)

#plot_histogram(NNs[0])
#print covs
print correlational_covariates(NNs,transmute(covs))

#scatter(get_mean_connectivity(NNs[0]))

#rows = ttest_square(NNs)
#for row in rows:
#	print row
#print len(rows)
#print len(rows[0])
#import numpy as np
#import matplotlib.pyplot as plt

#n = 1024
#X = np.random.normal(0, 1, n)
#Y = np.random.normal(0, 1, n)
#T = np.arctan2(Y, X)

#plt.axes([0.025, 0.025, 0.95, 0.95])
#plt.scatter(X, Y, s=75, c=T, alpha=.5)

#plt.xlim(-1.5, 1.5)
#plt.xticks(())
#plt.ylim(-1.5, 1.5)
#plt.yticks(())

#plt.show()
