import numpy as np

#Eingabe:
d = np.loadtxt('csv_data.csv', skiprows=1, delimiter=',')
quant_len = d.shape[0]
list_len = d.shape[1]
data = d.transpose()
quantities_and_units = [['$T$', '$\\eta$', '$\\tau$'], ['°C', 'mPas', 'Pa']]
err = np.array([[0.1 for _ in range(d.shape[1])], [0.1 for _ in range(d.shape[1])], [0.1 for _ in range(d.shape[1])]])
caption = 'Änderung der Viskosität bei Temperaturerhöhung'
label = 'Tabelle 1'


#Verarbeitung
def find_row_len():
    len = []
    for i in range(3,6):
        if list_len % i == 0:
            return i
        len.append(i - list_len % i)
    return len.index(min(len)) + 3


row_len = find_row_len()
col_len = list_len // row_len * quant_len
folds = list_len // row_len + (list_len % row_len > 0)

s = '\\begin{table}[h] \n\\centering \n\\caption{' + caption + '}\n\\begin{tabular}{|c||'
for i in range(row_len):
    s += 'c|'
s += '}\n'

for i in range(folds):
    s += '\\hline\n\\'
    for j in range(quant_len):
        s += quantities_and_units[0][j] + '(' + quantities_and_units[1][j] + ') '
        for k in range(row_len):
            k = k + row_len * i
            if k == list_len:
                s += '&'
                continue
            s += '& \\SI{' + str(data[j][k]) + ' \\pm ' + str(err[j][k]) + '}{} '
        s += '\\\\\n\\hline\n'
s += '\\end{tabular}\\label{tab: ' + label + '}\n'
s += '\\end{table}'

#Ausgabe
print(s)
text_file = open('tex_data.txt', "w")
text_file.write(s)
text_file.close()