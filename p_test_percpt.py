import perceptron_model_gen

"""
testing of model"""
a = perceptron_model_gen.Perceptron(test=True, w_file_name="p_weights.txt")
test_file_name = "test_data.txt"
# test = [22.727272727272727, 11, 122, 8, 4, 15, 78, 4.62, 4, 0]
# test=[22.727272727272727, 11, 115, 18, 3, 24, 89, 4.88, 1, 0]


test = [27.77777777777778, 9, 133, 15, 1, 14, 73, 4.59, 5, 0]  # --3
a.worker()
# print(a.weights_gen)

a.predict(test)
print(a.res)
