# get folder name 1  for sherlock holmes and get 2nd folder names with books for second author and third folder for 3rd author.

import getfiledata as f
from processa250data import info_on250words as info_obj
import pandas as pd
import random


def get_list_of_list_representation(folder_name, authid):
    data = f.return_string_data(folder_name, authid)
    # print(type(data))
    # print(type(data[0]))
    # print((data[0]))
    total_250_objs = 0
    total_list_of_objs = []
    # print(ord('”'))
    list_of_vector = []
    list_of_books_obj = []
    for j in range(0, len(data)):
        list_of_obj_250 = []
        for i in range(0, len(data[j])):
            lista = data[j][(j, i, authid)]
            k = info_obj(lista, 1, (j, i, authid))
            # print()
            list_of_obj_250.append(k)
        list_of_books_obj.append(list_of_obj_250)
    number_of_words_above_six = 0
    # print()
    for j in range(0, len(list_of_books_obj)):
        tup = 4, 579, 1
        list_of_obj_250 = list_of_books_obj[j]
        total_250_objs += len(list_of_obj_250)
        for i in range(0, len(list_of_obj_250)):
            obj = list_of_obj_250[i]
            total_list_of_objs.append(obj)
            list_of_vector.append(obj.return_a_vector())
            # if obj.id == tup:
            number_of_words_above_six += obj.no_stop
            # print(i, number_of_words_above_six)
            #     # print(obj.string_rep_of_data)
            # print(obj.no_ofw_per_line)

            # print(i, obj.id, obj.no_words_above_6, obj.most_used_word, obj.no_words_above_5, obj.no_ofwords,
            #       obj.average_word_length, obj.no_of_quotes, obj.no_of_ex, obj.no_stop)

    lisa = list(range(2168))
    print(len(total_list_of_objs))

    # for i in total_list_of_objs:
    #     print(i.id[2])
    #
    # print("********"*80)
    return list_of_vector
    # print(number_of_words_above_six, total_250_objs, number_of_words_above_six // total_250_objs)


def write_to_file(listof_data, filename):
    """
    we write the collected data to file to save time in future.
    :param listof_data:
    :param filename:
    :return:
    """

    length_of_individual_extracted_data = len(listof_data[1])
    string_to_save = str(length_of_individual_extracted_data) + "\n"
    for i in listof_data:
        for j in i:
            string_to_save += str(j) + ' '
        string_to_save += '\n'

    file1 = open(filename, "w")
    file1.write(string_to_save)

    file1.close()


def shuffle(list_of_data):
    shuffled_list = []
    for i in range(len(list_of_data) - 1):
        random_index = random.randint(0, len(list_of_data) - 1)
        shuffled_list.append(list_of_data.pop(random_index))
    shuffled_list.append(list_of_data.pop())
    return shuffled_list


def start_here():
    """
    we collect data for 3 authors
    give incremental ids and folder names where the books are located
    books should be .txt format.
    :return:
    """

    status = 2
    status = int(input("enter \n 1 for train \n 2 for test data"))
    listoflist1 = []
    authid = int(input("enter author id1"))
    folder_name = input("enter folder name")
    # authid = 1
    # folder_name = "datarandom"
    listoflist1.append(get_list_of_list_representation(folder_name, authid))
    authid = int(input("enter author id 2"))
    folder_name = input("enter folder name")
    # authid = 2
    # folder_name = "datarandom2"
    listoflist1.append(get_list_of_list_representation(folder_name, authid))
    authid = int(input("enter author id 3"))
    folder_name = input("enter folder name")
    # authid = 3
    # folder_name = "random3"
    listoflist1.append(get_list_of_list_representation(folder_name, authid))

    listoflist2 = []

    k = 1
    for i in listoflist1:
        for j in i:
            listoflist2.append(j)

    print(len(listoflist2))

    file_name = "data_extracted.txt"
    file_name_2 = "test_data.txt"

    if status == 1:
        # when 1 create data for training
        print("1", len(listoflist2))
        listoflist2 = shuffle(listoflist2)

        print("2", len(listoflist2))

        # write collected  data to a  file so saves time while creating and testing the tree
        write_to_file(listoflist2, file_name)
        df_record_set = pd.DataFrame(listoflist2, columns=['no_of_wdspline',
                                                           'no_of_lines',
                                                           'swords_count',
                                                           # 'no_of_ex',
                                                           # 'no_of_in',
                                                           'no_of_the',
                                                           'no_of_thats',
                                                           # 'no_of_quotes',
                                                           # 'no_of_ands',
                                                           'no_of_coma',
                                                           # 'no_of_q',
                                                           # 'no_of_a',
                                                           'no_of_words_above7',
                                                           'avg_wd_l',
                                                           # 'no_of_digits',
                                                           # 'No_of_vowels',
                                                           # 'NO_of_an',
                                                           'semi',
                                                           'colon',
                                                           # 'yeu',
                                                           # 'apos',
                                                           # 'no_of_sqb',
                                                           'authid'])

        df_record_set.to_csv('author_identification.csv')
    else:
        print("1", len(listoflist2))
        listoflist2 = shuffle(listoflist2)

        print("2", len(listoflist2))

        # write collected  data to a  file so saves time while creating and testing the tree
        write_to_file(listoflist2, file_name_2)

        df_record_set = pd.DataFrame(listoflist2, columns=['no_of_wdspline',
                                                           'no_of_lines',
                                                           'swords_count',
                                                           # 'no_of_ex',
                                                           # 'no_of_in',
                                                           'no_of_the',
                                                           'no_of_thats',
                                                           # 'no_of_quotes',
                                                           # 'no_of_ands',
                                                           'no_of_coma',
                                                           # 'no_of_q',
                                                           # 'no_of_a',
                                                           'no_of_words_above7',
                                                           'avg_wd_l',
                                                           # 'no_of_digits',
                                                           # 'No_of_vowels',
                                                           # 'NO_of_an',
                                                           'semi',
                                                           'colon',
                                                           # 'yeu',
                                                           # 'apos',
                                                           # 'no_of_sqb',
                                                           'authid'])

        df_record_set.to_csv('author_identification_test_data.csv')

    # we create a .csv file to cehck accuracy against the library version of tree


start_here()
