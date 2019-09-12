# we will look for following features
# 1 words sizes above 4
# 2 top 3 words
# 3 number of .
# 4number of ,
# 5 most favourite word
# number of !
# avergae word size
# totol number of words


"""
generates data for prediction
"""
from collections import Counter as c
import re
from nltk.stem.porter import PorterStemmer
from itertools import groupby
from nltk.corpus import stopwords


class info_on250words:
    __slots__ = ["data", "list_of_top_three_words", "dictionary_of_words", "no_stop", "no_words_above_4", "no_of_thats",
                 "no_of_q", "no_of_the", "no_of_that", "no_of_a", "digits", "no_of_vowels", "no_of_semi", "yeu_index",
                 "no_words_above_5", "no_words_above_6", "no_of_ex", "fav_word", "most_used_word", "no_ofc", "no_ofex",
                 "no_of_of", "no_of_quotes", "no_ofw_per_line", "no_of_sq", "no_of_an", "no_of_colon", "no_of_apos",
                 "no_of_sqb", "no_of_hype", "swords", "swords_count",
                 "no_ofwords", "authid", "string_rep_of_data", "average_word_length", "id", "no_of_ands", "no_of_or",
                 "no_of_in"]

    def __init__(self, string_list, auth_id, id):
        "input is string list"
        self.swords = set(stopwords.words("english"))
        self.swords_count = 0
        self.authid = auth_id
        self.id = id
        self.data = string_list
        self.list_of_top_three_words = []
        self.dictionary_of_words = {}  # unique words
        self.no_stop = 0
        self.no_ofc = 0
        self.most_used_word = ""
        self.no_words_above_4 = 0
        self.no_words_above_5 = 0
        self.no_words_above_6 = 0
        self.no_ofwords = 0
        self.no_of_an = 0
        self.no_of_ands = 0
        self.no_of_or = 0
        self.no_of_q = 0
        self.digits = 0
        self.no_of_the = 0
        self.no_of_colon = 0
        self.no_of_that = 0
        self.no_of_a = 0
        self.no_of_sqb = 0
        self.no_of_ex = 0
        self.no_of_in = 0
        self.no_of_apos = 0
        self.no_of_hype = 0
        self.no_of_of = 0
        self.no_of_vowels = 0
        self.no_of_that = 0
        self.yeu_index = 0
        self.no_of_sq = 0
        self.no_of_semi = 0
        self.string_rep_of_data = self.str_rep()
        self.average_word_length = 0
        self.no_of_quotes = 0
        # self.remove_common_words()
        self.no_ofw_per_line = 0
        self.create_a_dictionary_of_words()
        self.find_getmostandtop3()
        self.avglen()
        self.no_of_quotes += self.no_of_sq
        self.no_of_quotes = self.no_of_quotes // 2
        if self.no_stop != 0:
            self.no_ofw_per_line = self.no_ofwords / self.no_stop
        else:
            self.no_ofw_per_line = 0

        if self.no_of_ex > 0:
            self.no_of_ex = 1

        if self.no_of_q > 0:
            self.no_of_q = 1

        if self.digits > 0:
            self.digits = 1

        # self.yeu_index = self.yule(self.string_rep_of_data)

    def return_a_vector(self):
        vectored_rep = []
        # 1 add number of words per line
        # 2 add number of lines
        # 3 add number of exclmation
        # 4 add number of the
        # 5 add number of a
        # 6 add number of qu
        # 7 add number of words above 7
        vectored_rep.append(self.no_ofw_per_line)  # number of words per line
        vectored_rep.append(self.no_stop)  # no of lines
        vectored_rep.append(self.swords_count)  # no _of _swords
        # vectored_rep.append(self.no_of_ex)  # number of exclamation marks
        # vectored_rep.append(self.no_of_in)  # no of in
        vectored_rep.append(self.no_of_the)  # number of the
        vectored_rep.append(self.no_of_that)  # no of thats
        # vectored_rep.append(self.no_of_quotes)  # no of quotes
        # vectored_rep.append(self.no_of_ands)  # no of ands
        vectored_rep.append(self.no_ofc)  # nof of commas
        # vectored_rep.append(self.no_of_q)  # no of q
        # vectored_rep.append(self.no_of_a)  # no of a
        vectored_rep.append(self.no_words_above_6)  # no of words above 7
        vectored_rep.append(self.average_word_length)  # average word length
        # vectored_rep.append(self.digits)  # no of digits
        # vectored_rep.append(self.no_of_vowels)  # number of vowels
        # vectored_rep.append(self.no_of_an)  # no of ans
        vectored_rep.append(self.no_of_semi)
        vectored_rep.append(self.no_of_colon)  # number of colons
        # vectored_rep.append(self.yeu_index)  # yuele index
        # vectored_rep.append(self.no_of_apos)  # number of apostrophes
        # vectored_rep.append((self.no_of_sqb))  # number of squarebrackets
        vectored_rep.append(self.id[2])  # author id
        return vectored_rep

    def return_a_vector_test(self):
        vectored_rep = []
        # 1 add number of words per line
        # 2 add number of lines
        # 3 add number of exclmation
        # 4 add number of the
        # 5 add number of a
        # 6 add number of qu
        # 7 add number of words above 7
        vectored_rep.append(self.no_ofw_per_line)  # number of words per line
        vectored_rep.append(self.no_stop)  # no of lines
        vectored_rep.append(self.swords_count)  # no _of _swords
        # vectored_rep.append(self.no_of_ex)  # number of exclamation marks
        # vectored_rep.append(self.no_of_in)  # no of in
        vectored_rep.append(self.no_of_the)  # number of the
        vectored_rep.append(self.no_of_that)  # no of thats
        # vectored_rep.append(self.no_of_quotes)  # no of quotes
        # vectored_rep.append(self.no_of_ands)  # no of ands
        vectored_rep.append(self.no_ofc)  # nof of commas
        # vectored_rep.append(self.no_of_q)  # no of q
        # vectored_rep.append(self.no_of_a)  # no of a
        vectored_rep.append(self.no_words_above_6)  # no of words above 7
        vectored_rep.append(self.average_word_length)  # average word length
        # vectored_rep.append(self.digits)  # no of digits
        # vectored_rep.append(self.no_of_vowels)  # number of vowels
        # vectored_rep.append(self.no_of_an)  # no of ans
        vectored_rep.append(self.no_of_semi)
        vectored_rep.append(self.no_of_colon)  # number of colons
        # vectored_rep.append(self.yeu_index)  # yuele index
        # vectored_rep.append(self.no_of_apos)  # number of apostrophes
        # vectored_rep.append((self.no_of_sqb))  # number of squarebrackets
        return vectored_rep

    def words(self, entry):
        return filter(lambda w: len(w) > 0, [w.strip("0123456789!:,.?(){}[]") for w in entry.split()])

    def create_a_dictionary_of_words(self):
        for i in self.data:
            i = i.lower()
            length = len(i)
            if length >= 6:
                self.no_words_above_6 += 1
            elif length == 4:
                self.no_words_above_4 += 1
            elif length == 5:
                self.no_words_above_5 += 1

            if i in self.swords:
                self.swords_count += 1
            if i == "and":
                self.no_of_ands += 1
            elif i == "or":
                self.no_of_or += 1
            elif i == "in":
                self.no_of_in += 1
            elif i == "of":
                self.no_of_of += 1
            elif i == "that":
                self.no_of_that += 1
            elif i == "the":
                self.no_of_the += 1
            elif i == 'a':
                self.no_of_a += 1
            elif i == 'an':
                self.no_of_an += 1

            for j in i:
                if j == ".":
                    self.no_stop += 1
                elif j == "'" or ord(j) == 8216 or ord(j) == 8217:
                    self.no_of_sq += 1
                elif j == ",":
                    self.no_ofc += 1
                elif j == "'":
                    self.no_of_apos += 1
                elif j == ":":
                    self.no_of_colon += 1
                elif j == "!":
                    self.no_of_ex += 1
                elif j == "?":
                    self.no_of_q += 1
                elif j == "-":
                    self.no_of_hype += 1
                elif j == ";":
                    self.no_of_semi += 1
                elif j == "(" or j == ")":
                    self.no_of_sqb += 1
                elif ord(j) == 8220 or ord(j) == 8221 or j == '"':
                    self.no_of_quotes += 1
                if j.isdigit():
                    self.digits += 1
                j = j.lower()
                if j == 'a' or j == 'e' or j == 'i' or j == 'o' or j == 'u':
                    self.no_of_vowels += 1

            if self.dictionary_of_words.get(i.lower()) == None:
                self.dictionary_of_words[i.lower()] = 1
            else:
                self.dictionary_of_words[i.lower()] += 1
            self.no_ofwords += 1

    def avglen(self):
        sum = 0
        for i in self.data:
            sum += len(i)

        self.average_word_length = round(sum / len(self.data), 2)

    def find_getmostandtop3(self):
        most1 = 0
        most1_w = ""
        most2 = 0
        most2_w = ''
        most3 = 0, ""
        string_equ = ""
        for i in self.dictionary_of_words:
            a = self.dictionary_of_words[i]
            if a > most1:
                most1 = a
                most1_w = i

        for i in self.dictionary_of_words:
            a = self.dictionary_of_words[i]
            if a > most2 and a < most1:
                most2 = a
                most2_w = i

        self.most_used_word = most1_w
        # print(most1, most1_w, most2, most2_w)

    def str_rep(self):
        str_rep = ""
        for i in self.data:
            # for j in i:
            #     if ord(j) > 255 and ord(j) != 8220 and ord(j) != 8221 and ord(j)!= 8217 and ord(j)!=8216:
            #          print("yes", ord(j))
            str_rep += i.lower() + " "
        return str_rep

    def remove_common_words(self):
        a = chr(8221)
        b = "'" + str(a) + "'"
        listofstopwords = [r'\bthe\b', r"\bme\b", r"\bfor\b", r"\bin\b", r"\bdo\b", r"\bwhy\b", r"-", r"\ba\b",
                           r"\bit[s|'s]*\b", r"\bhe\b", r"\bhis\b", r"\bher\b", r"\bis\b", r"\bwe\b", r"\bas\b",
                           r"\bwas\b", r"\bwas\b",
                           r"\bi\b", r'\"|"\s*', r"\'", r"\bto\b", r'\,', r"\bhad\b", r"\byou\b", r"\.",
                           r"\bher\b", r"\band\b", r'“',
                           r"\bshe\b", r"\bmy\b", r"\bthat\b", r"\bof\b", r"\bwith\b", r'\bat\b', r'\bnot\b', r'\bso\b'
                                                                                                              r"\s+"]
        # print(re.sub(r"\bthe\b","", a))
        # print(re.sub("\ba\b", "", a))
        for i in listofstopwords:
            self.string_rep_of_data = re.sub(i, " ", self.string_rep_of_data)
        self.string_rep_of_data = self.string_rep_of_data.replace(a, "")
        self.data = self.string_rep_of_data.split()

        # A = 65
        # a = 97
        # z = 122
        # Z = 90
        # !=33
        # .=46
        # - =45
