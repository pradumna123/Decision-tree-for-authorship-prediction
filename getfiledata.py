import os


def read_a_file(file_name):
    with open(file_name, "r") as file:
        data = file.read()
        data = data.split()
    return data


def printa(h):
    print(h)


def processdata_250_word(string_data, init, aut_no):
    dictionary_of_data = {}
    start = 0
    index = 0
    for i in range(0, len(string_data), 250):
        a = init, index, aut_no
        dictionary_of_data[a] = string_data[i:i + 250]
        start += i
        index += 1
    return dictionary_of_data


def return_string_data(folder_name, init):
    folder_name_1 = folder_name
    currentpath = os.getcwd()
    path_1 = os.path.join(currentpath, folder_name_1)
    filesin_1 = os.listdir(path_1)

    final_data = []
    index = 0
    # index is file number
    for i in filesin_1:
        final_data.append(processdata_250_word(read_a_file(os.path.join(path_1, i)), index, init))
        index += 1

    return final_data


def test():
    folder_name = "datarandom"
    data = return_string_data(folder_name, 1)
    print(len(data))
    for i in data:
        for j in i:
            if len(i[j]) < 250:
                print(len(i[j]), j)

