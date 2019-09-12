import p_model
import numpy as np


""""
generates model
"""
class Perceptron:
    __slots__ = ["filename", "no_of_features", "data_list_of_list", "result", "result_list", "only_attr", "weights_gen",
                 "res", "test", "weight_file_name",
                 "no_of_uniqueclasses", "no_of_uniqueclasses_list", "p_model_obj", "result_list_for_uc"]

    def __init__(self, filename=None, test=False, w_file_name=None):
        self.filename = filename
        self.data_list_of_list = []
        self.test = test
        self.no_of_features = 0
        self.result = []
        self.result_list = []  # here we will have result list modified for each author .
        self.only_attr = []  # this will only contain attributes
        self.no_of_uniqueclasses = 0
        self.no_of_uniqueclasses_list = []  # this will contain unique class set values from result column.
        self.p_model_obj = []
        self.result_list_for_uc = []
        self.weights_gen = []
        self.weight_file_name = w_file_name
        self.res = []

    def worker(self):
        if self.test == True:
            self.read_file()
        else:
            self.process_file_andFsp_create_a_list()
            print(len(self.data_list_of_list))
            self.sep_the_result_and_attr()
            # print(self.result_list_for_uc)
            print('step2')
            self.find_number_of_uniqueclasses()
            print('step3')
            print(self.no_of_uniqueclasses_list)
            self.modify_result_list()
            print('end')

    def read_file(self):
        """
        this will read read the weights saved by model
        :return:
        """
        gen_we = []
        with open(self.weight_file_name, "r") as h:
            q = h.read()
            q = q.split("\n")
            # print(q)
            temp = []
            for i in q:
                temp = i.split()
                temp_2 = list(range(len(temp)))
                # print(temp)
                for z in range(len(temp)):
                    temp_2[z] = float(temp[z])
                gen_we.append(temp_2)
                temp = []
                temp_2 = []

        for i in gen_we:
            if len(i) > 1:
                self.weights_gen.append(i)

    def sep_the_result_and_attr(self):
        for i in self.data_list_of_list:
            self.result.append(i[-1])
            temp = i[:-1]
            self.only_attr.append(temp)
            temp = []

    def find_number_of_uniqueclasses(self):
        "here we find the number of unique classes "
        temp = []
        uniue_set = set(self.result)
        # print(uniue_set)
        self.no_of_uniqueclasses = len(uniue_set)
        self.no_of_uniqueclasses_list = list(uniue_set)
        return uniue_set

    def modify_result_list(self):
        """
        here we create 3 results lists tailored for each class.
        :return:
        """
        temp = []
        for i in self.no_of_uniqueclasses_list:
            for j in range(len(self.result)):
                if self.result[j] == i:
                    temp.append(i)
                else:
                    temp.append(0)
            self.result_list_for_uc.append(temp)
            temp = []

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

    def create_a_model(self):
        """run on one model"""
        print("train start")

        for i in range(self.no_of_uniqueclasses):
            a = p_model.P_cep(self.only_attr, self.result_list_for_uc[i], 70000, self.no_of_features)
            a.train_model()
            list_temp = a.return_weights()
            # print(list_temp)
            self.weights_gen.append(list_temp)

    def sigmiod(self, x):
        return 1 / (1 + np.exp(-x))

    def predict(self, vector):
        vector = np.array(vector)
        # vector = vector.reshape(vector.shape[0], -1)
        # intercept = np.ones((vector.shape[0], 1))
        # vector = np.concatenate((intercept, vector), axis=1)

        res = []
        sum = 0
        for i in range(len(self.weights_gen)):
            we_s = np.array(self.weights_gen[i])
            sum = np.dot(vector, we_s)
            # for j in range(len(we_s)):
            #     # print(we_s,vector)
            #     sum += vector[j] * we_s[j]
            sum = self.sigmiod(sum)
            res.append(sum)
            sum = 0

        self.res = res

    def save_weights_to_file(self):
        """write weights to file"""
        string = ""
        for i in self.weights_gen:
            for j in i:
                string += str(j) + " "
            string += "\n"

        with open("p_weights.txt", 'w') as f:
            f.write(string)


#

if __name__ == "__main__":
    filename = "data_extracted.txt"
    # test = [20.833333333333332, 12, 130, 19, 5, 18, 66, 4.61, 4, 0]  # -->2
    test = [1,27.77777777777778, 9, 133, 15, 1, 14, 73, 4.59, 5, 0]  # -->3
    b = Perceptron(filename)
    b.worker()
    b.create_a_model()
    b.predict(test)
    b.save_weights_to_file()

    print(b.res)

    # a = Perceptron(test=True)
    # a.worker()
    # # print(a.weights_gen)
    # a.predict(test)
    # print(a.res)
