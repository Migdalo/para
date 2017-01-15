"""
Cipher module encodes and decodes rotation cipher.
"""
from __future__ import print_function
import string

def discover_alphabet(convertable, nonumbers=False, addpunct=False):
    """ Get an alphabet range to use. """
    convertable = str(convertable)
    alphabet = []
    has_upper = False
    has_lower = False
    has_digits = False
    punct = []
    for char in convertable:
        if char not in alphabet:
            if char in string.ascii_lowercase:
                has_lower = True
            elif char in string.ascii_uppercase:
                has_upper = True
            elif not nonumbers and char in string.digits:
                has_digits = True
            elif addpunct and char not in string.digits:
                punct.append(char)
        if has_digits and has_lower and has_upper:
            break
        elif nonumbers and has_lower and has_upper:
            break

    if has_lower:
        alphabet.append(string.ascii_lowercase)
    if has_upper:
        alphabet.append(string.ascii_uppercase)
    if has_digits:
        alphabet.append(string.digits)
    if addpunct:
        alphabet.append(''.join(punct))
    return ''.join(alphabet)

def rotate(convertable, alphabet='', rot=13):
    """ Caesar cipher """
    plain = []

    if not alphabet:
        alphabet = discover_alphabet(convertable)

    if rot > len(alphabet):
        rot = rot - len(alphabet)

    for char in convertable:
        if char not in alphabet:
            plain.append(char)
        else:
            tmp = alphabet.index(char) + rot
            if tmp >= len(alphabet):
                tmp = tmp - len(alphabet)
            plain.append(alphabet[tmp])
    return ''.join(plain)

def solve_rotation(convertable, keyword=''):
    """ Print all possible rotations. """
    alphabet = discover_alphabet(convertable)
    print('{0: <5}'.format('ROT') + convertable)
    print('-' * 20)
    for i in range(len(alphabet)):
        if not keyword:
            print('{0: <5}'.format(str(i)) + rotate(convertable, alphabet, i))
        else:
            solution = rotate(convertable, alphabet, i)
            if keyword in solution:
                print('{0: <5}'.format(str(i)) + solution)
                return
