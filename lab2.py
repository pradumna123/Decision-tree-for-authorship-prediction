import create_a_tree_from_file
import perceptron_model_gen
import processa250data as pp

import sys

"""
class used to run models on test _data
"""


def read_user_file(filename):
    string_list = []
    with open(filename, "r")as f:
        data = f.read()
        data = data.split()
        # print(len(data))
        for i in data:
            if len(i) != 0:
                string_list.append(i)

        return string_list


def process_file_andFsp_create_a_list(filename):
    data_list_of_list = []
    no_of_features = 0
    with open(filename, 'r') as f:
        data = f.read()
        list_temp = data.split("\n")
        # print(type(list_temp[1]))
        list_single_attribute = []
        # print("!!!!!!", list_temp[0], len(list_temp[0]))
        for i in list_temp:
            if len(i) == 2:
                # print(i)
                no_of_features = int(i)
            if len(i) > 1:
                templist = i.split(" ")
                # print("!!", templist)
                if len(templist) > 1:
                    for att in templist:
                        if att != "":
                            if att.find('.') == -1:
                                list_single_attribute.append((int(att)))
                            else:
                                list_single_attribute.append(round(float(att), 3))
                    data_list_of_list.append(list_single_attribute)
                    list_single_attribute = []
    return no_of_features, data_list_of_list


def sep_the_result_and_attr(data_list_of_list):
    result = []
    only_attr = []
    for i in data_list_of_list:
        result.append(i[-1])
        temp = i[:-1]
        only_attr.append(temp)
        temp = []
    return result, only_attr


def create_tree_obj(filename):
    a = create_a_tree_from_file.grow_tree(filename)  # this is a class
    a.read_file(filename)  # this is a function to read and crearte a dictionary of n nodes.
    # a.print_data()
    # g = a.get_max(a.Serial_no, 0, len(a.Serial_no) - 1)
    # print(g)
    a.root = a.make_tree(a.Serial_no, 0, len(a.Serial_no) - 1)  # this function creates a tree.
    a.print_inorder(a.root)
    return a


def test_tree_obj(only_attr, result, tree_obj):
    """
    returns accuracy
    :param only_attr:
    :param result:
    :return:
    """
    total = len(only_attr)
    correct = 0
    for i in range(len(only_attr)):
        val = tree_obj.test(only_attr[i])
        if val == result[i]:
            correct += 1
    return correct / total


def make_percept_model(file3):
    a = perceptron_model_gen.Perceptron(test=True, w_file_name=file3)
    # test_file_name = "test_data.txt"
    a.worker()
    return a


def test_p_obj(only_attr, result, p_obj):
    # print(only_attr)
    # return
    # print("!!!!!!!!!!", result)

    total = len(only_attr)
    correct = 0
    for i in range(len(only_attr)):
        p_obj.predict(only_attr[i])
        lista = p_obj.res
        temp = lista[0]
        index = 0

        for j in range(1, len(lista)):
            if lista[j] > temp:
                temp = lista[j]
                index = j
        # max_val = int(max_val[0])
        index = index + 1
        # index=index[0]
        # print(lista, index, temp, type(index), type(temp), result[i])
        # print(lista, max_val, index, result[i])
        if index == result[i]:
            # print(index, result[i])
            correct += 1

    return correct / total


def main():
    # print(len(sys.argv))
    file1 = sys.argv[2]

    # print("!!!", file1)
    dict_auth = {1: "arthur", 2: "Melville", 3: "Austen"}
    # status = int(input("enter a value \n 1 for using test_data_file \n 2 for using a test data from your side."))
    # status = 1
    status = 2
    if status == 1:
        # "we will test 2 models on a single test_data."
        file1 = 'test_data.txt'

        file2 = 'alpha.txt'

        file3 = 'p_weights2.txt'

        # file1 = input("enter file name for test_data")
        # file2 = input("enter a file for  tree creation")
        # file3 = input("enter file name for perceptron creation")
        No_features, data_list = process_file_andFsp_create_a_list(file1)
        # for i in data_list:
        #     print(i)
        # print(data_list)
        result, only_attr = sep_the_result_and_attr(data_list)

        # create a object of tree
        tree_obj = create_tree_obj(file2)

        acc_tree = test_tree_obj(only_attr, result, tree_obj)

        print(acc_tree)

        P_obj = make_percept_model(file3)

        print(test_p_obj(only_attr, result, P_obj))

    if status == 2:
        # file1 = "delta"
        # file1 = input("enter file name for test_data")
        file2 = "alpha.txt"
        file3 = "p_weights2.txt"

        string_list = read_user_file(file1)
        obj_data = pp.info_on250words(string_list, 1, 1)
        vect = obj_data.return_a_vector_test()

        tree_obj = create_tree_obj(file2)

        val = tree_obj.test(vect)

        print("output of tree : ", dict_auth[val])

        #
        # P_obj = make_percept_model(file3)
        #
        # P_obj.predict(vect)
        # res = P_obj.res
        #
        # val1 = res[0]
        # index = 0
        #
        # for j in range(len(res)):
        #     if res[j] > val1:
        #         val1 = res[j]
        #         index = j

        # print("output of perceptron  ", dict_auth[index + 1])

        # print(vect)

        # No_features, data_list = process_file_andFsp_create_a_list(file1)

        # result, only_attr = sep_the_result_and_attr(data_list)

        # print(only_attr)
        # val=tree_obj.test(only_attr[0])
        # print(val,result[0])
        # print(type(val), type(result[0]))
        # tree_obj.print_inorder(tree_obj.root)
        # tree_obj.print_data()
        # print(len(tree_obj.Serial_no))


main()
