import string

""" Get an alphabet range to use. """
def discover_alphabet(convertable, nonumbers=False, addpunct=False):
    alphabet = []
    has_upper = False
    has_lower = False
    has_digits = False
    punct = []
    for c in convertable:
        if c not in alphabet:
            if c in string.ascii_lowercase:
                has_lower = True
            elif c in string.ascii_uppercase:
                has_upper = True
            elif not nonumbers and c in string.digits:
                has_digits = True
            elif addpunct and c not in string.digits:
                punct.append(c)
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

""" Caesar cipher """
def rotate(convertable, alphabet='', rot=13):
    plain = []
    
    if not alphabet:
        alphabet = discover_alphabet(convertable)
    
    if rot > len(alphabet):
        rot = rot - len(alphabet)
    
    try:
        for c in convertable:
            if c not in alphabet:
                plain.append(c)
            else:
                tmp = alphabet.index(c) + rot
                if tmp >= len(alphabet):
                    tmp = tmp - len(alphabet)
                plain.append(alphabet[tmp])
        return ''.join(plain)
    except:
        return ''

""" Print all possible rotations. """
def solve_rotation(convertable, keyword=''):
    alphabet = discover_alphabet(convertable)
    print '{0: <5}'.format('ROT'), convertable
    print '-' * 20
    for i in range(len(alphabet)):
        if not keyword:
            print '{0: <5}'.format(str(i)), rotate(convertable, alphabet, i)
        else:
            solution = rotate(convertable, alphabet, i)
            if keyword in solution:
                print '{0: <5}'.format(str(i)), solution
                return

