"""
this file will create the tree again from the file.
"""


class Node:
    __slots__ = ["column_no", "split_val", "left_node", "right_node", "are_you_root", 'majority_value', "sr_no"]

    def __init__(self, lsta):
        self.sr_no = lsta[0]
        self.left_node = lsta[1]
        self.right_node = lsta[2]
        self.column_no = lsta[3]
        self.split_val = lsta[4]
        self.majority_value = lsta[5]
        self.are_you_root = lsta[6]

    def get_lef_right(self):
        string = ""
        string += str(self.sr_no) + " "
        if self.left_node != None:
            string += str(self.left_node.sr_no) + " "
        else:
            string += "None" + " "
        if self.right_node != None:
            string += str(self.right_node.sr_no) + " "
        else:
            string += "None" + " "
        string += str(self.column_no) + " "
        string += str(self.split_val) + " "
        string += str(self.majority_value) + " " + str(self.are_you_root)
        string += "\n"

        return string


class grow_tree:
    __slots__ = ["data", "Serial_no", 'dict_a', 'filename', 'root', "string_from_file", 'string_generated', "sum"]

    def __init__(self, filename=None):
        self.filename = filename
        self.data = []
        self.Serial_no = []
        self.dict_a = {}
        self.root = None
        self.string_from_file = ""
        self.string_generated = ""
        self.sum = 0

    def read_file(self, filename):
        lista = []
        list_serial = []
        list_final = []
        dict_a = {}  # key as serial number and val as list of all thngs including sr_no
        with open(filename, "r") as f:
            data = f.read()
            self.string_from_file = data
            data = data.split("\n")
            # print(data)
            data_temp = []
            for i in data:
                if len(i) > 1:
                    data_temp.append(i)
            data = data_temp
            for i in data:
                i = i.split()
                # print(i)  # list of list with strings
                sr_no = int(i[0])
                list_serial.append(sr_no)
                for j in i:  # this is a list
                    if j == 'None':
                        lista.append(None)
                    elif j == 'True':
                        lista.append(True)
                    elif j == 'False':
                        lista.append(False)
                    else:
                        lista.append(float(j))
                dict_a[sr_no] = lista
                list_final.append(lista)
                lista = []

        self.Serial_no = list_serial
        self.data = list_final
        self.dict_a = dict_a

    def get_max(self, arr, strt, end):
        i, Max = 0, arr[strt]
        maxind = strt
        for i in range(strt + 1, end + 1):
            if arr[i] > Max:
                Max = arr[i]
                maxind = i
        return maxind

    def make_tree(self, inorder, start, end):
        if start > end:
            return None
        i = self.get_max(inorder, start, end)

        root = Node(self.dict_a.get(inorder[i]))

        if start == end:
            return root

        root.left_node = self.make_tree(inorder, start, i - 1)
        root.right_node = self.make_tree(inorder, i + 1, end)

        return root

    def print_data(self):
        # print(self.Serial_no)
        print(self.Serial_no)
        # print(self.dict_a)

    def print_inorder(self, node):
        if node == None:
            return
        self.print_inorder(node.left_node)
        self.print_inorder(node.right_node)
        self.string_generated += node.get_lef_right()
        self.sum += 1

    def test(self, attr):
        return int(self._test1(self.root, attr))

    def _test1(self, root, attr):
        # print(root)
        col_no = int(root.column_no)
        split_val = root.split_val

        if col_no == None:
            print("here")
            return

        if attr[col_no] <= split_val:
            if root.left_node != None:
                # if we have a node go ahead
                return self._test1(root.left_node, attr)
            else:
                # we have reached end.
                return int(root.majority_value)
        else:
            if root.right_node != None:
                return self._test1(root.right_node, attr)
            else:
                return int(root.majority_value)


def read_file(filename):
    pass


def main():
    file_test = 'tet.txt'
    file_name = "alpha.txt"
    a = grow_tree(file_name)  # this is a class
    a.read_file(file_name)  # this is a function to read and crearte a dictionary of n nodes.
    # a.print_data()
    # g = a.get_max(a.Serial_no, 0, len(a.Serial_no) - 1)
    # print(g)
    a.root = a.make_tree(a.Serial_no, 0, len(a.Serial_no) - 1)  # this function creates a tree.
    a.print_inorder(a.root)  # this will print a tree.

    test = [25.0, 10, 104, 16, 0, 27, 93, 5.15, 3, 2, 2]

    attribute = test[:len(test) - 1]
    val = test.pop(-1)
    print(type(val))
    v = a.test(attribute)
    print(v)
    print(v == val)

    # print(a.string_generated == a.string_from_file)
    # string = ''
    # alpha = a.string_from_file.split("\n")
    # for i in alpha:
    #     if len(i) > 1:
    #         temp = []
    #         temp = i.split()
    #         # print(temp)
    #         # break
    #         for j in temp:
    #             if j == 'None':
    #                 string += 'None' + " "
    #             elif j == 'True':
    #                 string += 'True' + " "
    #                 # lista.append(True)
    #             elif j == 'False':
    #                 string += 'False' + " "
    #                 # lista.append(False)
    #             else:
    #                 # aa = int((j))
    #                 aa = float(j)
    #                 string += str(aa) + ' '
    #                 # lista.append(float(j))
    #         string += '\n'
    # # print(alpha)
    # print(string == a.string_generated)
    # print(len(string), len(a.string_generated))
    # # print(string)
    # print(a.sum)

if __name__ == '__main__':
    main()
