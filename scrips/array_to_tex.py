import numpy as np
from scrips.tools import sci_round


def array_to_tex(array, error, quantities_and_units, caption='Table 1', label='Tabelle 1'):
    """
    Converts a 2D numpy array into a LaTeX table format.

    :param array: array_like, array containing the data to be converted.
    :param error: array_like, array containing the errors corresponding to the data.
    :param quantities_and_units: List, List of lists containing quantities and their units.
    :param caption: String, Caption for the LaTeX table.
    :param label: String, Label for referencing the table in LaTeX.
    """

    quant_len = array.shape[0]
    list_len = array.shape[1]

    # Processing
    def find_row_len():
        lengths = []
        for i in range(3, 6):
            if list_len % i == 0:
                return i
            lengths.append(i - list_len % i)
        return lengths.index(min(lengths)) + 3

    row_len = find_row_len()
    col_len = list_len // row_len * quant_len
    folds = list_len // row_len + (list_len % row_len > 0)

    #Scientific rounding of errors
    for i in range(quant_len):
        for j in range(list_len):
            array[i][j], error[i][j] = sci_round(array[i][j], error[i][j])

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
                s += '& \\SI{' + str(array[j][k]) + ' \\pm ' + str(error[j][k]) + '}{} '
            s += '\\\\\n\\hline\n'
    s += '\\end{tabular}\\label{tab: ' + label + '}\n'
    s += '\\end{table}'

    # Output
    print(s)
    text_file = open('tex_data.txt', "w")
    text_file.write(s)
    text_file.close()


def csv_to_tex(file, error, quantities_and_units, caption, label):
    """
    Converts a CSV file into a LaTeX table format.
    :param file: String, path to the CSV file.
    :param error: [...], [...], ...
    :param quantities_and_units: [q1, q2], [u1, u2]
    :param caption:
    :param label:
    :return:
    """
    #Eingabe:
    d = np.loadtxt(file, skiprows=1, delimiter=',')
    data = d.transpose()
    quant_len = data.shape[0]
    list_len = data.shape[1]
    #err = np.array([[round_up(0.1 * np.sqrt(2), 2) for _ in range(data.shape[1])], [round_up(np.sqrt(8), 1) for _ in range(data.shape[1])]])


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
                s += '& \\SI{' + str(data[j][k]) + ' \\pm ' + str(error[j][k]) + '}{} '
            s += '\\\\\n\\hline\n'
    s += '\\end{tabular}\\label{tab: ' + label + '}\n'
    s += '\\end{table}'

    #Ausgabe
    print(s)
    text_file = open('tex_data.txt', "w")
    text_file.write(s)
    text_file.close()

'''
quantities_and_units = [['$t$', '$U$'], ['s', 'mV']]
#err = np.array([[round_up(0.1 * np.sqrt(2), 2) for _ in range(data.shape[1])],
#                [round_up(np.sqrt(8), 1) for _ in range(data.shape[1])]])
caption = 'Amplitude bei Luftdämpfung'
label = 'Tabelle 1'
csv_to_tex('csv_data.csv', 3, quantities_and_units, caption, label)
'''