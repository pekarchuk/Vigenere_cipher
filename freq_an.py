#! /usr/bin/python3.3
# -*- coding:utf-8 -*-

from math import log2

def read_file():
    with open('book2.txt', 'r', encoding='utf-8') as f:
        z = f.read()
    return z


def prepare_text(z):
    """Deletes all non-alphabet symbols from text"""
    alphabet_str = "абвгдежзийклмнопрстуфхцчшщъыьэюя "
    z = list(' '.join(z.lower().split()))
    for i,k in enumerate(z):
        if k not in alphabet_str:
            z[i] = ''
    return ''.join(z)


def remove_spaces(z):
    return z.replace(" ", "")


def char_frequency(check_string):
    """Frequency analysis, returns frequency of letters, returns ('symbol', occurrences) """
    res_dict = dict()
    for s in check_string:
        if s in res_dict:
            res_dict[s] += 1
        else:
            res_dict[s] = 1
    return res_dict


def bigrams_frequency(check_string):
    """Frequency analysis, returns frequency of bigrams of letters, returns ('bigram', occurrences) """
    res_dict = dict()
    for i in range(len(check_string) - 1):
        bigram=check_string[i: i + 2]
        if bigram in res_dict:
            res_dict[bigram] += 1
        else:
            res_dict[bigram] = 1
    return res_dict


def bigrams_frequency_uncrossed(check_string):    
    """Frequency analysis, returns frequency of uncrossed bigrams, returns ('bigram', occurrences) """
    res_dict = dict()
    for i in range(0, len(check_string), 2):
        bigram = check_string[i:i+2]
        if bigram in res_dict:
            res_dict[bigram] += 1
        else:
            res_dict[bigram] = 1
    return res_dict


def entropy (freq_dict, text):
    return abs(round(sum((i/len(text)*log2(i/len(text)) for i in freq_dict.values())), 3))


def entropy_bi (freq_dict, text):
    return abs(round(sum((i/len(text)*log2(i/len(text)) for i in freq_dict.values()))/2, 3))


def redundancy(entropy):  
    return round(1 - (entropy / 5), 3)


def analysis(check_string):
    """Prins entropy and redudancy for letters and bigrams in text"""
    print("For letters: ")
    entropy1 = entropy(char_frequency(check_string),check_string)
    print("entropy = ", entropy1 )
    print("redundancy = ", redundancy  (entropy1))

    print("For bigrams: ")
    entropy2 = entropy_bi(bigrams_frequency(check_string),check_string)
    print("entropy = ", entropy2 )
    print("redundancy = ", redundancy(entropy2))



def main():
    """_____ lab 1: Frequency analysis of some text _____"""
    check_string = read_file()
    check_string = prepare_text(check_string)
    # removing spaces if necessary
    check_string = remove_spaces(check_string)
    
    #____________check char frequency_______________
    # result = sorted(char_frequency(check_string).items(), key=lambda x: (-x[1], x[0]))
    # for e in result: print(e, round(e[1]/len(check_string),4))
    #____________check bigram frequency_____________
    # 1) all bigrams
    # result = sorted(bigrams_frequency_uncrossed(check_string).items(), key=lambda x: (-x[1], x[0]))
    # 2) only uncrossed bigrams
    # result = sorted(bigrams_frequency(check_string).items(), key=lambda x: (-x[1], x[0]))
    # for e in result:  print(e, round(e[1]/len(check_string),5))
    # print (len(result)/6)

    #________finding entropy and redudancy__________
    analysis(check_string)


if __name__ == '__main__':
    main()
