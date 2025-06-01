import numpy as np

#Eingabe:
d = np.loadtxt('csv_data.csv', skiprows=1, delimiter=',')
d = d.transpose()
quantities_and_units = [['$T$', '$\\eta$', '$\\tau$'], ['°C', 'mPas', 'Pa']]
data = np.array(d)
err = np.array([[0.1 for _ in range(d.shape[1])], [0.1 for _ in range(d.shape[1])], [0.1 for _ in range(d.shape[1])]])
caption = 'Änderung der Viskosität bei Temperaturerhöhung'
label = 'Tabelle 1'


#Verarbeitung
s = '\\begin{table}[h] \n\\centering \n\\caption{' + caption + '}\n\\begin{tabular}{|c||'
for i in range(data.shape[1]):
    s += 'c|'
s += '}\n\\hline\n'
for i in range(data.shape[0]):
    s += quantities_and_units[0][i] + '(' + quantities_and_units[1][i] + ') '
    for j in range(data.shape[1]):
        s += '& \\SI{' + str(data[i][j]) + ' \\pm ' + str(err[i][j]) + '}{} '
    s += '\\\\\n\\hline\n'
s += '\\end{tabular}\\label{tab: ' + label + '}\n'
s += '\\end{table}'

#Ausgabe
print(s)
text_file = open('tex_data.txt', "w")
text_file.write(s)
text_file.close()