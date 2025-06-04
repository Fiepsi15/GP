import numpy as np
from tools import round_up

def array_to_tex(file, error, quantities_and_units, caption, label):
    #Eingabe:
    d = np.loadtxt(file, skiprows=1, delimiter=',')
    data = d.transpose()
    quant_len = data.shape[0]
    list_len = data.shape[1]
    #quantities_and_units = [['$t$', '$U$'], ['s', 'mV']]
    err = np.array([[round_up(0.1 * np.sqrt(2), 2) for _ in range(data.shape[1])], [round_up(np.sqrt(8), 1) for _ in range(data.shape[1])]])
    #caption = 'Amplitude bei Luftdämpfung'
    #label = 'Tabelle 1'

    data[1] = data[1] / 2

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

    s = '\\begin{table}[H] \n\\centering \n\\caption{' + caption + '}\n\\begin{tabular}{|c||'
    for i in range(row_len):
        s += 'c|'
    s += '}\n'

    for i in range(folds):
        s += '\\hline\n'
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


quantities_and_units = [['$t$', '$U$'], ['s', 'mV']]
#err = np.array([[round_up(0.1 * np.sqrt(2), 2) for _ in range(data.shape[1])],
#                [round_up(np.sqrt(8), 1) for _ in range(data.shape[1])]])
caption = 'Amplitude bei Luftdämpfung'
label = 'Tabelle 1'
array_to_tex('csv_data.csv', 3, quantities_and_units, caption, label)
