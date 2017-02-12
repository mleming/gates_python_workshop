import random
from scipy import stats
import csv


matrix_size = 116
num_subjs = 50;
covariate_labels = ['Age','Sex','Handedness','SMFQ']

# Create matrix files
for i in range(num_subjs):
	T = [[random.random() for x in range(matrix_size)] for x in range(256)]
	PN = [[0 for x in range(matrix_size)] for x in range(matrix_size)]
	for k in range(matrix_size):
		for j in range(matrix_size):
			(r,p)  = stats.pearsonr(T[k][:],T[j][:])
			PN[k][j] = r;
	csvfile = "/Users/mleming/Desktop/LFP/Pearson_files/" + str(i) + ".csv"
	with open(csvfile,"w") as output:
		writer = csv.writer(output, lineterminator='\n')
		writer.writerows(PN)
	print i

# Create covariate files
covariates = [[random.random() for x in range(num_subjs + 1)] for x in range(len(covariate_labels))]
covariates[0] = [x *5 + 12 for x in covariates[0]]
covariates[1] = [1 if x > 0.5 else 0 for x in covariates[1]]
covariates[2] = [(x*2)-1 for x in covariates[2]]
covariates[3] = [int(x*40) for x in covariates[3]]

for i in range(len(covariate_labels)):
	covariates[i][0] = covariate_labels[i]

csvfile = "/Users/mleming/Desktop/LFP/covs.csv"
covariates = [list(i) for i in zip(*covariates)] # Transmute matrix
with open(csvfile,"w") as output:
	writer = csv.writer(output, lineterminator='\n')
	writer.writerows(covariates)
