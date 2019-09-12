import pickle

from start import solver

pickle_in = open("treeclassifier.pickle", "rb")

a = pickle.load(pickle_in)

# a.printTree()
print(a.root)