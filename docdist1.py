# docdist1.py
# Author: Ronald L. Rivest
# Date Last Modified: February 14, 2007
# Changelog:
#   Version 1:
#     Initial version
#
# Usage:
#    docdist1.py filename1 filename2
#     
# This program computes the "distance" between two text files
# as the angle between their word frequency vectors (in radians).
#
# For each input file, a word-frequency vector is computed as follows:
#    (1) the specified file is read in
#    (2) it is converted into a list of alphanumeric "words"
#        Here a "word" is a sequence of consecutive alphanumeric
#        characters.  Non-alphanumeric characters are treated as blanks.
#        Case is not significant.
#    (3) for each word, its frequency of occurrence is determined
#    (4) the word/frequency lists are sorted into order alphabetically
#
# The "distance" between two vectors is the angle between them.
# If x = (x1, x2, ..., xn) is the first vector (xi = freq of word i)
# and y = (y1, y2, ..., yn) is the second vector,
# then the angle between them is defined as:
#    d(x,y) = arccos(inner_product(x,y) / (norm(x)*norm(y)))
# where:
#    inner_product(x,y) = x1*y1 + x2*y2 + ... xn*yn
#    norm(x) = sqrt(inner_product(x,x))

import math
    # math.acos(x) is the arccosine of x.
    # math.sqrt(x) is the square root of x.

import string
    # string.join(words,sep) takes a given list of words,
    #    and returns a single string resulting from concatenating them
    #    together, separated by the string sep .
    # string.lower(word) converts word to lower-case

import sys

##################################
# Operation 1: read a text file ##
##################################
def read_file(filename):
    """ 
    Read the text file with the given filename;
    return a list of the lines of text in the file.
    """
    try:
        fp = open(filename)
        L = fp.readlines()  #reading all the lines in the file
    except IOError:
        print "Error opening or reading input file: ",filename
        sys.exit()
    return L

#################################################
# Operation 2: split the text lines into words ##
#################################################
def get_words_from_line_list(L):
    """
    Parse the given list L of text lines into words.
    Return list of all words found.
    """

    word_list = []
    for line in L:
        words_in_line = get_words_from_string(line)
        word_list = word_list + words_in_line
    return word_list

def get_words_from_string(line):
    """
    Return a list of the words in the given input string,
    converting each word to lower-case.

    Input:  line (a string)
    Output: a list of strings 
              (each string is a sequence of alphanumeric characters)
    """
    word_list = []          # accumulates words in line
    character_list = []     # accumulates characters in word
    for c in line:                              
        if c.isalnum():
            character_list.append(c)                    # if it's an alphabet or number, append to character_list array, form it to a "word"
        elif len(character_list)>0:                     # if not alphabet or number && character_list is not empty (done collecting char in a word)
            word = string.join(character_list,"")       # add a "" to the end of the "word" consists of everything from character_list[]
            word = string.lower(word)                   # use all lower cases
            word_list.append(word)                      # add the "word" to word_list[]
            character_list = []                         # reinitialize character_list for the next "word"
    if len(character_list)>0:                   # done with the word 
        word = string.join(character_list,"")           # why is this neccessary
        word = string.lower(word)
        word_list.append(word)
    return word_list

##############################################
# Operation 3: count frequency of each word ##
##############################################
def count_frequency(word_list):
    """
    Return a list giving pairs of form: (word,frequency)
    """
    L = []
    for new_word in word_list:
        for entry in L:             # for every entry[] in L[], 
            if new_word == entry[0]:        # check if new_word can be matched to any entry[0] in L[]
                entry[1] = entry[1] + 1     # if entry is matched, add 1 to entry[1](the count of the entry[0])
                break
        else:
            L.append([new_word,1])          # if no match of entry in L[], add new entry to L[] with entry[1](count of the entry[0]) to 1
    return L        # L[] is a 2 dimensional array {(a,1003), (an, 600), (boy, 3)....}

###############################################################
# Operation 4: sort words into alphabetic order             ###
###############################################################
def insertion_sort(A):
    """
    Sort list A into order, in place.

    From Cormen/Leiserson/Rivest/Stein,
    Introduction to Algorithms (second edition), page 17,
    modified to adjust for fact that Python arrays use 
    0-indexing.
    """
    for j in range(len(A)):         # to iterate over the indices of a sequence, combine range() and len(), j would start with 0(due to the range() use)
        key = A[j]                  # A[0], A[1], A[2]
        # insert A[j] into sorted sequence A[0..j-1]
        i = j-1                     # set i to the last sorted list
        while i>-1 and A[i]>key:    # starting from the end of the sorted list going back(large to small), while current "key" still larger than A[i], keep going toward A[0]
            A[i+1] = A[i]           # move A[i] that is greater than key to A[i+1] to give in space for key between A[0] and A[i]
            i = i-1                 # i going forward toward 0
        A[i+1] = key                # found the i where A[i] is smaller than key and set A[i+1] to key
    return A
    
#############################################
## compute word frequencies for input file ##
#############################################
def word_frequencies_for_file(filename):
    """
    Return alphabetically sorted list of (word,frequency) pairs 
    for the given file.
    """

    line_list = read_file(filename)
    word_list = get_words_from_line_list(line_list)         # returns an array
    freq_mapping = count_frequency(word_list)               # return 2 dimensional array with (words, count)
    insertion_sort(freq_mapping)

    print "File",filename,":",
    print len(line_list),"lines,",
    print len(word_list),"words,",
    print len(freq_mapping),"distinct words"

    return freq_mapping

def inner_product(L1,L2):
    """
    Inner product between two vectors, where vectors
    are represented as alphabetically sorted (word,freq) pairs.

    Example: inner_product([["and",3],["of",2],["the",5]],
                           [["and",4],["in",1],["of",1],["this",2]]) = 14.0 
    """
    sum = 0.0           # floating point
    i = 0
    j = 0
    while i<len(L1) and j<len(L2):                  # go through every word in both files
        # L1[i:] and L2[j:] yet to be processed
        if L1[i][0] == L2[j][0]:                    # comparing the words
            # both vectors have this word
            sum += L1[i][1] * L2[j][1]              # Distance Metric, product of the counts
            i += 1
            j += 1
        elif L1[i][0] < L2[j][0]:
            # word L1[i][0] is in L1 but not L2  (L1[i][1] * L2[j][1]=0)
            i += 1
        else:
            # word L2[j][0] is in L2 but not L1  (L1[i][1] * L2[j][1]=0)
            j += 1
    return sum

def vector_angle(L1,L2):
    """
    The input is a list of (word,freq) pairs, sorted alphabetically.

    Return the angle between these two vectors.
    """
    numerator = inner_product(L1,L2)
    denominator = math.sqrt(inner_product(L1,L1)*inner_product(L2,L2))
    return math.acos(numerator/denominator)

def main():
    if len(sys.argv) != 3:
        print "Usage: docdist1.py filename_1 filename_2"
    else:
        filename_1 = sys.argv[1]
        filename_2 = sys.argv[2]
        sorted_word_list_1 = word_frequencies_for_file(filename_1)
        sorted_word_list_2 = word_frequencies_for_file(filename_2)
        distance = vector_angle(sorted_word_list_1,sorted_word_list_2)
        print "The distance between the documents is: %0.6f (radians)"%distance

if __name__ == "__main__":
    main()

    
    



