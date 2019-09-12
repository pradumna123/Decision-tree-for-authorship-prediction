from main import data_processing as dp
import timeit as t

import pickle


class Node:
    """
    this is a class that represents the node of the tree classifier
    """
    __slots__ = ["left_node", "right_node", "data_obj", "data_for_left", "data_for_right", 'current_depth',
                 'expr_entropy', "root_status", 'dict_current_level', "node_status", 'sum', "do_not_count", "sr_no",
                 "class_entropy", 'column_no', 'split_value', 'data_for_this_level', 'previous_data_obj', 'exp_depth']

    def __init__(self, old_obj, cureent_depth, node_status=None, rootstatus=False, sr_no=None):
        self.previous_data_obj = old_obj  # reference of previous data object
        self.root_status = rootstatus  # this will help us to create a root node.
        self.current_depth = cureent_depth  # the current depth of tree.
        # self.exp_depth = exp_depth  # expected  depth of tree 0 based so always +1
        # self.expr_entropy = expr_entropy  # expected entropy cutoff given by user
        # self.root_status = rootstatus
        self.data_for_left = []
        self.do_not_count = None
        self.data_for_right = []
        self.sr_no = sr_no
        self.left_node = None  # left node
        self.right_node = None  # right node
        self.node_status = node_status  # 1 for left and 0 for right
        self.class_entropy = 0
        self.sum = 0
        self.column_no = 0
        self.split_value = 0
        # print("node at level ::: ", self.current_depth)
        # self.functions_to_invoke()

    def get_lef_right(self):
        string = ""
        string += str(self.sr_no) + " "
        if self.left_node != None:
            if self.left_node.do_not_count != None:
                string += str(self.left_node.sr_no) + " "
        else:
            string += "None" + " "
        if self.right_node != None:
            if self.right_node.do_not_count != None:
                string += str(self.right_node.sr_no) + " "
        else:
            string += "None" + " "
        string += str(self.column_no) + " "
        string += str(self.split_value) + " "
        string += str(self.data_obj.get_majority_class()) + " " + str(self.root_status)
        string += "\n"

        return string

    def __str__(self):
        string = ""
        string = str(self.sr_no)
        string += " node is at current depth is :" + str(
            self.current_depth) + " node id is: " + str(self.current_depth) + str(
            self.node_status) + ' column no is :' + str(
            self.column_no) + " split_value is " + str(self.split_value) + '***' + str(self.data_obj.l_dict) + "\n"
        return string

    def functions_to_invoke(self):
        # special case for root node -> job is to parse the file.
        if self.root_status == True:
            self.do_not_count = False
            self.data_obj = self.previous_data_obj  # create a root object.
            self.data_obj.worker()  # we call this to address various functions in this data bj
            self.column_no, self.split_value = self.data_obj.get_row_with_highest_entropy()
            if self.column_no == None:
                self.do_not_count = None  # here we ge row with highest_entropy and splitvalue
                return False
            self.dict_current_level = self.data_obj.return_adict_()  # returns the dictionary of used Values.
            self.data_for_left, self.data_for_right = self.data_obj.get_split_data_set()  # we store the divided dataset for future node use
            self.class_entropy = self.data_obj.total_entropy
            return True
        else:
            # create a object
            # normal node

            left, right = self.previous_data_obj.get_split_data_set()
            if self.node_status == 1:
                data = left  # when this is left node
                if len(data) < 1:
                    print("!!!!!!!!!!", len(data))

                    return False

            else:
                data = right  # when this is right node
                if len(data) < 1:  # somehow no data.
                    print("!!!!!!", len(data))

                    return False

            self.data_obj = dp(None, self.previous_data_obj.return_modified_dicr(), self.previous_data_obj,
                               )  # here we create a new

            self.data_obj.size_of_data()

            self.data_obj.set_data(data)
            status = self.data_obj.worker()
            if status == False:
                # returns false if the  the dataset has only 1 category of result.
                return False
            self.dict_current_level = self.data_obj.return_modified_dicr()
            self.column_no, self.split_value = self.data_obj.get_row_with_highest_entropy()
            self.data_for_left, self.data_for_right = self.data_obj.get_split_data_set()
            # print(self.current_depth, self.data_obj, len(data))  # we store the divided dataset for future node use
            self.dict_current_level = self.data_obj.return_adict_()
            print(self.current_depth, self.data_obj, len(data),
                  self.data_obj.l_dict)  # returns the dictionary of used Values.
            self.class_entropy = self.data_obj.total_entropy  # we save the entropy here.
            self.do_not_count = False
            return True


class solver:
    """
    we will create a tree here
    """
    __slots__ = ["dict_of_used_values", "root", 'root_of_tree', 'entropy_set', "serialnum", 'sum', "final_string",
                 "depth_set"]

    def __init__(self, expected_depth=9, expected_entropy=None, filename1=None):
        dp_for_root = dp(filename1, None, None, root=True)
        self.serialnum = 0
        # print(dp_for_root.filename)
        self.root = Node(dp_for_root, 0, rootstatus=True, sr_no=self.serialnum)
        # self.serialnum += 1
        self.root.functions_to_invoke()
        # self.root = dp(filename1, None, None, root=True)  # this will be root .
        # self.root.data_obj.worker()
        # self.dict_of_used_values = self.root.data_obj.return_adict_()
        # self.root.data_obj.g_dict = self.dict_of_used_values
        # self.root.data_obj.copy_g_dict()
        self.root_of_tree = self.root
        self.depth_set = expected_depth
        self.entropy_set = expected_entropy
        self.sum = 0

        self.final_string = ''

        # send depth+1

    def Create_tree(self):
        self.ct(self.root, 1)

    def ct(self, node, depth):
        if depth == self.depth_set:
            return  # when the depth is excedded

        self.serialnum += 1
        temp = Node(node.data_obj, depth,
                    node_status=1, sr_no=self.serialnum)
        status = temp.functions_to_invoke()
        if status == True:
            node.left_node = temp
            self.ct(node.left_node, depth + 1)
        else:
            self.serialnum -= 1
            return
        self.serialnum += 1
        temp = Node(node.data_obj, depth, node_status=0, sr_no=self.serialnum)
        status = temp.functions_to_invoke()

        if status == True:
            node.right_node = temp
            self.ct(node.right_node, depth + 1)
        else:
            self.serialnum -= 1
            return
        return

    def printTree(self):
        self.final_string += self.root.get_lef_right()
        self.printtreea(self.root)

    def printstart(self):
        # self.root.sr_no = 0
        self.printtree23(self.root)

    def printtree23(self, node):
        """
        give sr_no to nodes
        :param node:
        :return:
        """
        if node != None and node.do_not_count != None:
            self.printtree23(node.left_node)

            self.printtree23(node.right_node)
            node.sr_no = self.sum
            self.sum += 1

    def printstart555(self):
        # self.final_string += self.root.get_lef_right()
        self.printtree235555(self.root)

    def printtree235555(self, node):
        if node != None and node.do_not_count != None:
            self.printtree235555(node.left_node)

            # node.sr_no = self.sum
            self.final_string += node.get_lef_right()

            self.printtree235555(node.right_node)

    def printtreea(self, node):
        # if node != None and node.do_not_count != None:

        if node.left_node != None:
            if node.left_node.do_not_count != None:
                self.printtreea(node.left_node)
            else:
                return

        else:
            return

        node.sr_no = self.sum
        # self.final_string += node.get_lef_right()
        self.sum += 1

        # print(node, "!!!!", self.sum)

        if node.right_node != None:
            if node.left_node.do_not_count != None:
                self.printtreea(node.right_node)
            else:
                return
        else:
            return
        # print(node)

    def printTree1(self):
        # self.final_string += self.root.get_lef_right()
        self.printtreea(self.root)

    def printtreea1(self, node):
        if node.left_node != None:
            if node.left_node.do_not_count != None:
                self.printtreea(node.left_node)
        else:
            return

        # node.sr_no = self.sum
        self.final_string += node.get_lef_right()
        # self.sum += 1

        # print(node, "!!!!", self.sum)

        if node.right_node != None:
            if node.left_node.do_not_count != None:
                self.printtreea(node.right_node)
            else:
                return
        else:
            return
        # print(node)

    def test(self, attr):
        return self._test1(self.root, attr)

    def _test1(self, root, attr):
        # print(root)
        col_no = root.column_no
        split_val = root.split_value

        if col_no == None:
            print("here")
            return

        if attr[col_no] <= split_val:
            if root.left_node != None:
                if root.left_node.do_not_count != None:
                    # if we have a node go ahead
                    return self._test1(root.left_node, attr)
            else:
                # we have reached end.
                return root.data_obj.get_majority_class()
        else:
            if root.right_node != None:
                if root.right_node.do_not_count != None:
                    return self._test1(root.right_node, attr)
            else:
                return root.data_obj.get_majority_class()

        # print(root.data_obj.get_majority_class())


"""
testing data
"""
# test = [22.727272727272727, 11, 115, 18, 3, 24, 89, 4.88, 1, 0, 2]
# test=[27.77777777777778 ,9 ,133, 15, 1, 14, 73, 4.59, 5, 0, 3]
# test = [22.727272727272727, 11, 122, 8, 4, 15, 78, 4.62, 4, 0, 3]
# test = [20.833333333333332, 12, 130, 19, 5, 18, 66, 4.61, 4, 0, 2]
test = [25.0, 10, 104, 16, 0, 27, 93, 5.15, 3, 2, 2]

attribute = test[:len(test) - 1]
val = [-1]

filename = input("enter a filename to generate tree from: ")
depth = input("enter the depth of tree")
# filename = "data_extracted.txt"
a = solver(filename1=filename)
"this methods creates the tree"
a.Create_tree()
a.depth_set = depth
print("##################################################################")
a.printstart()
a.printstart555()

print("num of nodes", a.sum)
print(a.test(attribute))

# pickle_out = open("treeclassifier.pickle", "wb")
# pickle.dump(a, pickle_out)
# pickle_out.close()

"""
writing the tree to a file
"""
text_file = open("alpha.txt", "w")
text_file.write(a.final_string)
text_file.close()

# print("saved object")
# # print(a.root.data_obj)
