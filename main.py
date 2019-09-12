import math

"""

#### set number of uniue classes  at root when processing data for first time.


steps to do after creating this object.
1process file
2checkdata()
3sep_the_result_and_attr()
4find_number_of_uniqueclasses()
5calculate_total_entropy()
6 calculate the class with highest infogain
    initiailize the dict_of_used_rows. or get it from the global obj.
    scroll through start i.e only attr
"""


class data_processing:
    __slots__ = ["filename", "data_list_of_list", "total_enteries", "no_of_features", "dict_of_used_att_index",
                 "are_you_root", "old_data_obj", "column_no", "split_value", "f_left", "f_right",
                 "no_of_uniqueclasses_list", 'set_of_unique_vales',
                 "only_attr", "result", "no_of_uniqueclasses", "total_entropy", "g_obj", "g_dict", "l_dict",
                 "count_of_uniqueclasses"]

    def __init__(self, filename, gdict, old_d_obj, g_obj=None, root=False):
        self.old_data_obj = old_d_obj  # this will hold the object for the previous data object in tree.
        self.are_you_root = root  # this will act as a flag for root
        self.filename = filename  # this is the filename from which the data will be extracted used only at root.
        self.g_dict = gdict  # this is the global version of the dictionary
        self.data_list_of_list = []  # holds the data for the given node.
        self.column_no = 0  # holds the column number for which the spilt value should be applied.
        self.split_value = 0  # holds the split value of the node
        self.total_enteries = 0  # total data ponits at this node
        self.no_of_features = 0  # this is the "length" (1-based) of the entire vector passed to the tree.
        self.no_of_uniqueclasses = 0  # this will be the number of global unique classes in the entire dataset.
        self.dict_of_used_att_index = {}  # will hold a list of gloabl dict to stop attribute resuse
        self.only_attr = []  # holds only the attribute after the separation of data
        self.result = []  # holds the result values after separation of dataset
        self.total_entropy = 0  # this holds the entripy for the class. to be calculated upon initialzeation
        # this is the global_dataset obj of this is None i.e this is global dataset
        self.g_obj = g_obj  # a reference to the global copy .
        self.l_dict = {}  # a clocal copy of the global dictionary instance

        self.f_left = []  # this will hold the data after splitting for the next left node.
        self.f_right = []  # this will hold the data after splitting for future right node.

        self.no_of_uniqueclasses_list = []
        self.count_of_uniqueclasses = []
        self.set_of_unique_vales = None

    def __str__(self):
        string = ''
        string += "len of data : " + str(len(self.data_list_of_list)) + " column no :" + str(
            self.column_no) + "split_value" + str(self.split_value) + "total_entropy" + str(
            self.total_entropy) + "no of unq classes :" + str(self.no_of_uniqueclasses) + "total_enteries " + str(
            self.total_enteries)

        return string

    def get_majority_class(self):
        self.no_of_uniqueclasses_list = list(set(self.result))
        for i in self.no_of_uniqueclasses_list:
            self.count_of_uniqueclasses.append(self.result.count(i))

        temp = 0
        class_no = 0
        for i in range(len(self.count_of_uniqueclasses)):
            if self.count_of_uniqueclasses[i] > temp:
                # shift
                temp = self.count_of_uniqueclasses[i]
                class_no = self.no_of_uniqueclasses_list[i]

        return class_no

    def set_data(self, data):
        self.data_list_of_list = data
        if len(data) >= 1:
            self.no_of_features = len(self.data_list_of_list[0])

    def return_modified_dicr(self):
        return self.l_dict

    def worker(self):
        if self.are_you_root == True:
            self.process_file_andFsp_create_a_list()
        # self.display_data_set()
        self.check_data()
        self.sep_the_result_and_attr()
        # self.printonlyattr()
        self.find_number_of_uniqueclasses()
        status = self.calculate_total_entropy()

        if status == False:
            return False

        if self.are_you_root == False:
            self.copy_g_dict()
        else:
            self.l_dict = self.return_adict_()  # creating a dict for first time

    def copy_g_dict(self):
        for i in self.g_dict:
            self.l_dict[i] = self.g_dict[i]

    def assign(self):
        self.set_of_unique_vales = set(self.result)

    def get_split_data_set(self):
        """
        this method will return the bifurcated dataset.based on the row and split value
        :returns left,right and respective results rl and rr
        :return: 
        """""
        left = []
        right = []

        for i in self.data_list_of_list:
            if i[self.column_no] <= self.split_value:
                left.append(i)
            else:
                right.append(i)

        self.f_left = left
        self.f_right = right

        return left, right

    def process_file_andFsp_create_a_list(self):
        with open(self.filename, 'r') as f:
            data = f.read()
            list_temp = data.split("\n")
            # print(type(list_temp[1]))
            list_single_attribute = []
            # print("!!!!!!", list_temp[0], len(list_temp[0]))
            for i in list_temp:
                if len(i) == 2:
                    # print(i)
                    self.no_of_features = int(i)
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
                        self.data_list_of_list.append(list_single_attribute)
                        list_single_attribute = []

    def size_of_data(self):
        self.total_enteries = len(self.data_list_of_list)
        return self.total_enteries

    def display_data_set(self):
        for i in self.data_list_of_list:
            print(i)

    def check_data(self):
        for i in self.data_list_of_list:
            if len(i) != self.no_of_features:
                print("error while parsing", len(i))
                print(self.no_of_features)

    def sep_the_result_and_attr(self):
        for i in self.data_list_of_list:
            self.result.append(i[-1])
            temp = i[:-1]
            self.only_attr.append(temp)
            temp = []

    def printonlyattr(self):
        for i in self.only_attr:
            print(i)

    def find_number_of_uniqueclasses(self):
        "here we find the number of unique classes "
        temp = []
        uniue_set = set(self.result)
        # print(uniue_set)
        self.no_of_uniqueclasses = len(uniue_set)
        return uniue_set

    def get_unique_values_in_the_row(self, column_no):
        """returns the uniue values based on the column numbers send to it"""
        extracted_list = [row[column_no] for row in self.data_list_of_list]
        # print(len(extracted_list))
        unique_values = set(extracted_list)
        return unique_values, len(unique_values)

    def get_count(self, number_to_count, column_number):
        """
        row no from 0
        to be used on globlal dataset
        :param number_of_count:
        :param row_number:
        :return:
        """

        # print(number_to_count,column_number)
        extracted_list = [row[column_number] for row in self.data_list_of_list]
        occurence = extracted_list.count(number_to_count)
        return occurence

    def calculate_total_entropy(self):
        """
        we calculate class level entropy here for the result
        execute the seperator
        :return:
        """
        total = float(len(self.data_list_of_list) - 1)
        num_of_unique = []
        # here we will get the number of unique value set
        no_of_unique_value = self.find_number_of_uniqueclasses()
        for i in no_of_unique_value:
            # here we will find the occurrence of those unique values
            num_of_unique.append(self.result.count(i))

        if len(no_of_unique_value) == 1:
            self.total_entropy = 0
            return 0

        # we calculate the entropy
        value = 0
        for i in num_of_unique:
            temp_a = (i / total)
            if temp_a != 0:
                value += -(temp_a * (math.log(temp_a, self.no_of_uniqueclasses)))
            else:
                value += 0

        self.total_entropy = value

        return value

    def return_adict_(self):
        """used only for global data attribute"""
        temp_duict = {}
        for i in range(self.no_of_features - 2):
            temp_duict[i] = False
        return temp_duict

    def extract_column_from_the_dataset(self, column_no):
        """
        return the column  from the data set .
        :param column_no:
        :return:
        """
        extracted_list = [row[column_no] for row in self.data_list_of_list]
        return extracted_list

    def give2_list_left_and_right(self, extracted_column, threshold):
        # theshold is the avg value from the calling funcrtion
        # here given column number we will split the column into 2 parts one with values
        # below or equal to threshold and other with values above the threshold.
        # return the newly created list.
        extracted_column_temp = extracted_column
        left = []
        right = []
        resultl = []
        resultr = []
        for i in range(len(extracted_column_temp)):
            if extracted_column_temp[i] <= threshold:
                left.append(extracted_column_temp[i])
                resultl.append(self.result[i])
            else:
                right.append(extracted_column_temp[i])
                resultr.append(self.result[i])

        # helper check
        if len(left) != len(resultl) and len(right) != len(resultr):
            print("something wrong")

        return left, resultl, right, resultr

    def _entropcal(self, uniquevalue_count):
        """
        here we calculate the entropy
        :param uniquevalue_count: a list of number of instancs of the unique classes
        :return:
        """

        # print(uniquevalue_count)
        # we a count of uniue numbers. for ex if 4 i.e something has 4 instances of it in that particular column.
        total = 0
        base_log = len(uniquevalue_count)
        no_of_uniqueclass = self.no_of_uniqueclasses
        entropy = 0
        for i in uniquevalue_count:
            total += i

        if len(uniquevalue_count) == 1:
            return 0
        for i in range(len(uniquevalue_count)):
            if uniquevalue_count[i] == 0:
                return 0
            p1 = ((uniquevalue_count[i]) / total)
            # print(p1, uniquevalue_count[i], total)
            entropy += -(p1) * (
                math.log(p1, base_log))

        return entropy

    def calculate_entropy(self, resultl, resultr):
        """
        we will calculate the info gain here.
        ##
        :param left:
        :param resultl:
        :param right:
        :param resultr:
        :return:
        """
        total = len(resultr) + len(resultl)
        p1 = len(resultr) / total
        p2 = len(resultl) / total
        inst_r = []  # a list of instances
        inst_l = []  # a list of instances
        set_r = set(resultr)  # here we get unique values R
        set_l = set(resultl)  # here we get unquie values L

        # here we have worked out the problem of having ony one class in our left or right result,
        # so we dont have  a problem into entropy calculation
        for i in set_r:
            inst_r.append(resultr.count(i))

        for i in set_l:
            inst_l.append(resultl.count(i))
        if len(inst_l) > 1:
            entropyl = self._entropcal(inst_l)
        else:
            entropyl = 0
        if len(inst_r) > 1:
            entropyr = self._entropcal(inst_r)
        else:
            entropyr = 0

        # calculate the gain.

        gain = self.total_entropy - (p1 * entropyr) - (p2 * entropyl)
        # we return gain.
        return gain

    def do_binary_work(self, column_number):
        """
        here we do binary classification
        :param column_number:
        :return:
        """
        val_1 = []
        val_0 = []

        data_from_column = self.extract_column_from_the_dataset(column_number)

        for i in range(len(data_from_column)):
            if data_from_column[i] == 1:
                val_1.append(self.result[i])
            else:
                val_0.append(self.result[i])

        gain = self.calculate_entropy(val_1, val_0)
        return gain

    def do_extra(self, set_of_unique_values, column_number):
        # extract the column form the dataset.
        extratced_column = self.extract_column_from_the_dataset(column_number)

        # now sort the set_of_uniue value and start spliting
        dict_store_temp = {}
        set_of_unique_values1 = set_of_unique_values
        set_of_unique_values1.sort()

        # now start by taking avg of 2 number serialy from start and calculate the entropy for the changed
        # set and return the split poitcwith highest entropy along with
        # entropy
        for k in range(len(set_of_unique_values1)):
            starting_number = set_of_unique_values1[k]
            for i in range(1, len(set_of_unique_values1) - 1):
                if i == k:
                    # we dont calculate when they are same
                    continue
                second_number = set_of_unique_values1[i]
                avg = (starting_number + second_number) / 2
                left, resultl, right, resultr = self.give2_list_left_and_right(extratced_column, avg)

                # calculate entropy
                gain = self.calculate_entropy(resultl, resultr)
                dict_store_temp[(starting_number, second_number, avg, i)] = gain

        # we have gain for all combinations now.
        # print("***", dict_store_temp)
        # find the highest gain.
        gain_temp = 0
        avg_tmep = 0
        for i in dict_store_temp:
            temp = dict_store_temp[i]
            if temp > gain_temp:
                gain_temp = temp
                avg_tmep = i[2]

        # here we return the gain and the split value.
        return gain_temp, avg_tmep

    # store the highest value info gain.
    # create a tuple of (num1,num2, avg and entropy) for value and key as column number .
    # we calculated the average -> split the current column in 2 on the avg and see the entropy.

    def get_row_with_highest_entropy(self):
        """
        here we scroll through all arttributes and  find the highest entropy
        :return: 1 column_no and split_value --> when the attribute column with highest entropy has multiple values ex 1,2,3,4,5,6...etc....
                2 column_no and None --> when the column with highest entropy has only 2 values i.e 1 and 0
        """
        did_we_change_any_value = False
        # this dictionary will conatain key as row no and value as corresponding calculated entropy
        entropy_calculation_dictionary = {}
        for i in range(self.no_of_features - 2):
            # first check if the row is used in previous iteration
            if self.l_dict[i] == True:
                # used move ahead
                continue
            else:
                # now we have a row that is not used so we calculate its entropy
                # 2 ways if the row has 2 unique values go ahead and calculate entropy .
                # if the row has more unique values process it.
                # unique values.

                # set and len we get
                # set_of_values --> these are the possible values the particular,
                # attribute can take on ex-- [1,2,3,2.3,3.4,,,etc]
                set_of_values, no_of_unique = self.get_unique_values_in_the_row(i)

                if no_of_unique > 2:
                    # do extra processing

                    gain_temp, split_value = self.do_extra(list(set_of_values), i)
                    # print("we get______", gain_temp)
                    entropy_calculation_dictionary[i] = [gain_temp, split_value]
                elif no_of_unique == 2:
                    # do binary processing
                    gain_temp = self.do_binary_work(i)
                    entropy_calculation_dictionary[i] = [gain_temp, None]
                else:
                    # the attribute has only one value throughout ,kind of useless attribute column so we skip it.
                    continue

        # find the column with highest gain
        # print("!!!!!!!!!!!@@@@@@@@@@@@", entropy_calculation_dictionary)
        if len(entropy_calculation_dictionary) == 0:
            return None, None
        gain_temp = 0
        split_value1 = 0
        column_no = 0
        for i in entropy_calculation_dictionary:
            list_of_values = []
            list_of_values = entropy_calculation_dictionary[i]
            gain_value, split_value = list_of_values[0], list_of_values[1]
            if gain_value >= gain_temp:
                gain_temp = gain_value
                column_no = i
                split_value1 = split_value

        # now we have the split value and the column number return it
        self.column_no = column_no
        self.split_value = split_value1
        self.l_dict[column_no] = True
        self.assign()
        return column_no, split_value1
