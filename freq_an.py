#! /usr/bin/python3.3
# -*- coding:utf-8 -*-

from itertools import islice, chain
from math import log2
import collections


def prepare_text(filename):
    """Deletes all non-alphabet symbols from text"""
    alphabet_str = "абвгдежзийклмнопрстуфхцчшщъыьэюя "
    with open(filename, 'r', encoding='utf-8') as f:
        z = f.read()
    z = list(' '.join(z.lower().split()))
    z = [x for x in z if x in alphabet_str]
    return ''.join(z).replace(" ", "")


def char_frequency(check_string):
    """Frequency analysis, returns frequency of letters, returns ('symbol', occurrences) """
    return collections.Counter(check_string)


def bigrams_frequency(check_string):
    """Frequency analysis, returns frequency of bigrams of letters, returns ('bigram', occurrences) """
    bigr = zip(check_string, islice(check_string, 1, None))
    return collections.Counter(e1 + e2 for e1, e2 in bigr)


def bigrams_frequency_uncrossed(check_string):
    """Frequency analysis, returns frequency of uncrossed bigrams, returns ('bigram', occurrences) """
    bigr = zip(check_string, islice(check_string, 2, None))
    return collections.Counter(e1 + e2 for e1, e2 in bigr)


def entropy(freq_dict, text):
    return abs(round(sum(i / len(text) * log2(i / len(text)) for i in freq_dict.values()), 3))


def entropy_bi(freq_dict, text):
    return abs(round(sum(i / len(text) * log2(i / len(text)) for i in freq_dict.values()) / 2, 3))


def redundancy(entropy):
    return round(1 - (entropy / 5), 3)


def analysis(check_string):
    """Prints entropy and redudancy for letters and bigrams in text"""
    print("For letters: ")
    entropy1 = entropy(char_frequency(check_string), check_string)
    print("entropy = ", entropy1)
    print("redundancy = ", redundancy(entropy1))

    print("For bigrams: ")
    entropy2 = entropy_bi(bigrams_frequency(check_string), check_string)
    print("entropy = ", entropy2)
    print("redundancy = ", redundancy(entropy2))


def main():
    """_____ lab 1: Frequency analysis of some text _____"""
    filename = 'book2.txt'
    check_string = prepare_text(filename)

    # ____________check char frequency_______________
    # result = char_frequency(check_string)
    # for e in result:
    #     print(e, round(e[1] / len(check_string), 4))
    # ____________check bigram frequency_____________
    # 1) all bigrams
    # result = bigrams_frequency_uncrossed(check_string)
    # 2) only uncrossed bigrams
    # result = bigrams_frequency(check_string)
    # for e in result:
    #     print(e, round(e[1] / len(check_string), 5))
    # print(len(result)/6)

    # ________finding entropy and redudancy__________
    analysis(check_string)


if __name__ == '__main__':
    main()
