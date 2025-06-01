import numpy as np

#Eingabe:
d = np.loadtxt('csv_data.csv', skiprows=1, delimiter=',')
d = d.transpose()
quant_len = d.shape[0]
list_len = d.shape[1]
quantities_and_units = [['$T$', '$\\eta$', '$\\tau$'], ['°C', 'mPas', 'Pa']]
data = np.array(d)
err = np.array([[0.1 for _ in range(d.shape[1])], [0.1 for _ in range(d.shape[1])], [0.1 for _ in range(d.shape[1])]])
caption = 'Änderung der Viskosität bei Temperaturerhöhung'
label = 'Tabelle 1'


#Verarbeitung
def find_row_len():
    len = []
    for i in range(3,6):
        if list_len % i == 0:
            return i
        len.append(i)
    return max(len)


row_len = find_row_len()
col_len = list_len // row_len * quant_len

s = '\\begin{table}[h] \n\\centering \n\\caption{' + caption + '}\n\\begin{tabular}{|c||'
for i in range(row_len):
    s += 'c|'
s += '}\n\\hline\n'
for i in range(col_len):
    n = i % quant_len
    s += quantities_and_units[0][n] + '(' + quantities_and_units[1][n] + ') '
    for j in range(row_len):
        m = j + i // quant_len * quant_len
        s += '& \\SI{' + str(data[n][m]) + ' \\pm ' + str(err[n][m]) + '}{} '
    s += '\\\\\n\\hline\n'
s += '\\end{tabular}\\label{tab: ' + label + '}\n'
s += '\\end{table}'

#Ausgabe
print(s)
text_file = open('tex_data.txt', "w")
text_file.write(s)
text_file.close()