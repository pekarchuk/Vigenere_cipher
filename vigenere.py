#! /usr/bin/python3.3
# -*- encoding: utf-8 -*-


def prepare_text(z):
    """Deletes all non-alphabet symbols from text"""
    alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    # alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    z = list(' '.join(z.upper().split()))
    for i,k in enumerate(z):
        if k not in alphabet:
            z[i] = ''
    return ''.join(z)


def encode(plaintext, key):
    """Vigenere cipher, returns CT"""
    alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    # alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    result = []
    for i,k in enumerate(plaintext):
        sym_index = alphabet.find(k)
        key_index = alphabet.find(key[i%len(key)])
        res_index = (key_index + sym_index)%len(alphabet)
        result.append(alphabet[res_index])
    return ''.join(result)
    

def decode(CT, key):
    """Decoding Vigenere, returns PT"""
    alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    # alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    result = []
    for i,k in enumerate(CT):
        sym_index = alphabet.find(k)
        key_index = alphabet.find(key[i%len(key)])
        res_index = (sym_index - key_index)%len(alphabet)
        result.append(alphabet[res_index])
    return ''.join(result)


def index (CT): 
    """Returns matching index of text"""
    alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    # alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    N = (CT.count(t) * (CT.count(t) - 1) for t in alphabet)
    I = sum(N) / (len(CT) * (len(CT) - 1))
    return round(I, 5)


def find_small_key_length (CT):    
    """Returns length of key (for short ones: 2, 3, 4, 5)"""
    text_index_ru = 0.0553
    text_index_en = 0.0644

    diff = dict()
    for r in range(2,6):       
        y_r = divide_text(CT, r)
        Ir_arr = [index(e) for e in y_r]
        res = round(sum(Ir_arr) / len(Ir_arr), 5)
        diff[r] = round(abs(text_index_ru - res), 3)
        print ('r =',r, 'index =', res, 'mod =', round(abs (text_index_ru - res),3))
    return min(diff, key=diff.get)


def divide_text(text, r):
    """Divides text to r parts, returns array of strings"""
    return [text[i::r] for i in range(r)]


def matches_bigram_start(ciphertext):
    """Analysing bigrams frequency in text, returns [('MB', (38, 2))] in descending order"""
    bigrams_count_dict = dict()
    bigram_new = dict()
    bigrams = [ciphertext[i:i+2] for i in range(0, len(ciphertext), 2)]
    for e in set(bigrams):
        if bigrams.count(e) != 1:
            bigrams_count_dict[e] = [bigrams.count(e)]
    for bigram in bigrams_count_dict:
        bigram_index = [i for i,ltr in enumerate(bigrams) if ltr == bigram]
        bigram_index_diff = [bigram_index[a+1] - bigram_index[a] for a in range(0,len(bigram_index)-1)]
        if all(x == bigram_index_diff[0] for x in bigram_index_diff):
            bigram_new[bigram] = (bigram_index_diff[0], len(bigram_index_diff))
    return sorted(bigram_new.items(), key=lambda x: (x[1][1], x[0]), reverse=True)


def matches_stat(ciphertext, r):
    """Finds letter matches on k-distance, returns number_of_matches"""
    return sum((1 if x == ciphertext[k+r] else 0 for k,x in enumerate(ciphertext[:-r])))


def matches_dict_func(ciphertext, k):
    """ Finds letter matches on k-distance, returns paird (distanse, number_of_matches) in descending order"""
    matches_dict = [(x, matches_stat(ciphertext, x)) for x in range(6, k + 1)]
    return sorted(matches_dict, key=lambda x: (-x[1], x[0]))


def find_key_length(match_d):
    """Returns item with max value in dictioinary"""
    return max(match_d, key= lambda x: x[-1])


def char_frequency(check_string):
    """ Frequency analysis, returns frequency of letters in descending order """
    res_dict = dict()
    for s in check_string:
        if s in res_dict:
            res_dict[s] += 1
        else:
            res_dict[s] = 1
    return sorted(res_dict.items(), key=lambda x: (-x[1], x[0]))
        

def decipher(CT):
    """Deciphering of Vigenere cipher (work function for long keys)"""
    # alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

    # most frequent chars 
    freq_english = "ETAINOSHRDLUCMFWYGPBVKQJXZ"
    russian_freq = "ОАЕИНТРСЛВКПМУДЯЫЬГЗБЧЙХЖШЮЦЩЭФЪ"
    
    # finding the length of key
    # 1) check symbol's matches (input max distance of checking)
    print("\n Matched symbols distances: ")
    print(    matches_dict_func(CT, 33) )
    # 2) check distance between repeated bigrams and number of such repeats
    # print("\n Repeated bigrams distances: ")
    # print(    matches_bigram_start(CT) )
    # guessing the length of the key
    r = int(input("\n Input assumed length of the key: r = "))

    # divide text to parts (r parts)
    divided_text_arr = divide_text(CT, r)

    # finding subkeys (in each part) + trying with recieved key
    e = 0
    while True:
        sub_key = []
        for i in divided_text_arr:
            y = char_frequency(i)[0][0]
            # k_english = chr((ord(y) - 65 - ord(freq_english[e]) - 65) % len(alphabet) + 65)
            k_russian = chr((ord(y) - 1040 - ord(russian_freq[e]) - 1040) % len(alphabet) + 1040)
            sub_key.append(k_russian)

        assumed_key = ''.join(sub_key).upper()
        print(sub_key)
        print("Trying with key: ", assumed_key)
        print (decode(CT, assumed_key))       #prints decoded text
        ifyesorno = int(input("Is this it? (1/0): "))
        e += 1
        if ifyesorno:
            print("Your key is: ", assumed_key, "\n Great job!")
            break


def main():
    """_____ lab 1: Vigenere cipher _____"""
    key = u"ЭКОМАЯТНИКФУКО"
    # print(len(key))

    # if reading plaintext from file
    with open('plaintext.txt', 'r', encoding='utf-8') as f:
        PT = f.read()
    PT = prepare_text(PT)
    
    # Test for encoding
    # CT = encode(PT, key)
    CT = decode(PT, key)
    # print(CT)

    # Test for fining key length (for shorn ones)
    # print(find_small_key_length(CT))
    # print(index(CT))
    # print(matches_dict_func(CT))

   
if __name__ == '__main__':
    main()