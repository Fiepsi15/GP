

def max_index(data):
    '''
    Calculate the index of the maximum value in ``data``.
    :param data: array
    :return: index of the maximum value
    '''
    i_0, current_max = 0, 0
    for i in range(len(data)):
        if data[i] > current_max:
            current_max = data[i]
            i_0 = i
    return i_0
