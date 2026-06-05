import numpy as np
from Biophysik.gene_expression.subscripts import cell_growth
from Biophysik.gene_expression.subscripts import protein_quantification


data_directory = 'Biophysik/gene_expression/'

# Growth Analysis
data = np.loadtxt(data_directory + 'growth_data.csv', skiprows=1, delimiter=',').transpose()
t = data[0] * 60  # t in s
OD_600 = data[1]
cell_growth.calculate_doubleling_coefficient(t, OD_600)

# Protein Quantification:
data = np.loadtxt(data_directory + 'SpektrenG5.csv', skiprows=2, delimiter=',', usecols=[0, 1, 8, 9],
                  max_rows=351).transpose()
Baseline = data[:2]
Sample = data[-2:]
protein_quantification.absorption_quantification(Baseline, Sample)

#Photoconversion

