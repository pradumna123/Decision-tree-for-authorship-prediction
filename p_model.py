import numpy as np


class P_cep:
    __slots__ = ["data", "result", "weights", "iter", "fit_extra", "th", "features", "lr", "data_size"]

    def __init__(self, data, result, iteration, features, lr=0.001):
        """

        :param data:
        :param result:
        :param iteration:
        :param features:
        :param lr: learning rate
        """
        # print(result)
        self.data_size = len(data)
        self.data = data
        if isinstance(self.data, np.ndarray):
            pass
        else:
            self.data = np.array(self.data)
            y = np.ones(self.data.shape[0]).reshape(self.data.shape[0], -1)
            print("shape of y is ", y.shape)
            self.data = np.append(y, self.data, axis=1)
            print("shpe of data is ",self.data.shape)
        self.result = result
        # print(self.result)
        if isinstance(self.result, np.ndarray):
            result.reshpae(-1, 1)
        else:
            self.result = np.array(self.result).reshape(-1, 1)
            # self.result = self.result.reshape(-1, 1)
        # print("!!!!!!!!!!!!", self.result.shape)
        # print("#######"*80)
        # print(self.result)

        self.features = features

        # print("@@@@@@@@@@@@@@@", self.features)
        # self.weights = 2 * np.random.random((self.features, 1)) - 1

        # self.weights = self.weights.astype('float64')

        self.iter = iteration
        # print(len(self.data), len(self.result))

        self.lr = lr
        # self.weights = np.zeros(self.data.shape[1])
        # self.weights = self.weights.reshape(self.weights.shape[0], -1)
        self.weights = np.random.random((self.features, 1))

    def generate_loss(self, h, y):
        """

        :param h: predicted
        :param y: actual
        :return:
        """
        # print("shape of predicted is ", h.shape, "shape of actual is ", y.shape,"data size ", self.data_size)
        logprobs = np.multiply(np.log(h), y) + np.multiply((1 - y), np.log(1 - h))
        cost = - np.sum(logprobs) / self.data_size
        # a = -((1 / self.data_size) * ( np.sum( ((y * np.log(h) - (1 - y) * np.log(1 - h))))))
        # print("printing loss", a)
        return cost

    def return_weights(self):
        wei = self.weights.tolist()
        list_temp = []
        for i in wei:
            for j in i:
                list_temp.append(j)

        # add intercept i.e extra bias point
        # self.data = self.data.reshape(self.data.shape[0], -1)
        # intercept = np.ones((self.data.shape[0], 1))
        # self.data = np.concatenate((intercept, self.data), axis=1)

        return list_temp

    def sigmiod(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivation(self, x):
        return x * (1 - x)

    def threshold(self):
        th = np.average(self.result)

    def train_model(self):

        for i in range(self.iter):
            print("iteration number ", i)
            temp1 = np.dot(self.data, self.weights)
            temp1 = self.sigmiod(temp1)
            #before sending to generate loss make sure to remodel it.   to 1 and 0
            temp1 = np.where(temp1 >= 0.5 , 1 , 0)
            print(temp1)

            self.weights = self.weights-((self.lr/self.data_size)*(np.dot((temp1-self.result).T,self.data).T))

            print("loss at end of training is ", self.generate_loss(temp1, self.result))













    #
    #
    #
    #     # print("^^^^^^^^^^^^^^", self.weights.shape)
    #     # print(self.data.shape)
    #     for i in range(self.iter):
    #         inl = self.data
    #         out = self.sigmiod(np.dot(inl, self.weights))
    #         error = inl - out
    #         adj = error * self.sigmoid_derivation(out)
    #         # print(inl.shape, adj.shape)
    #         a = np.dot(inl.T, adj)
    #         # print("&&&&&&&&&", a.shape)
    #         # self.weights -=
    # # as
    # #         # inl = self.data
    #         # # print("1", inl.shape)
    #         # sig_out = self.sigmiod(np.dot(inl, self.weights))
    #         # grad = np.dot(self.data.T, (sig_out - self.result)) / self.result.size
    #         #
    #         # # print("!!!!", grad.shape, self.weights.shape)
    #         # self.weights.T -= self.lr * grad

    # temp = np.dot(self.data, self.lr)
    # j = self.sigmiod(temp)
    # loss = self.generate_loss(j, self.result)

    # # print("2", sig_out.shape)
    # err = self.result - sig_out
    # # print("3", err.shape)
    # adj = err * self.sigmoid_derivation((sig_out))
    # # print("adj", adj.shape)
    # self.weights += np.dot(inl.T, adj)
