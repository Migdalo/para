import base64
import string
import binascii

""" 
Convert the input from integer to ascii text and return it. If unsuccesfull, 
return an empty string. 
"""
def integer_to_ascii(convertable):
    try:
        return chr(int(convertable))
    except:
        return ''

""" 
Convert the input from ascii to integer and return it. If unsuccesfull, 
return an empty string. 
"""
def ascii_to_integer(convertable):
    try:
        return ord(convertable)
    except:
        try:
            numbers = []
            for i in convertable:
                numbers.append(ord(i))
            return numbers
        except:
            return ''

""" 
Convert the input from integer to hex and return it. If unsuccesfull, 
return an empty string. 
"""
def integer_to_hex(convertable):
    try:
        return hex(int(convertable))[2:]
    except:
        return ''
    
""" 
Convert the input from hex to integer and return it. If unsuccesfull, 
return an empty string. 
"""
def hex_to_integer(convertable):
    try:
        return int(convertable, 16)
    except:
        return ''

""" 
Convert the input from ascii text to hex and return it. If unsuccesfull, 
return an empty string. 
"""
def ascii_to_hex(convertable):
    try:
        return convertable.encode('hex')
    except:
        return ''
   
""" 
Convert the input from hex to ascii text and return it. If unsuccesfull, 
return an empty string. 
""" 
def hex_to_ascii(convertable):
    try:
        return convertable.decode('hex')
    except:
        return ''

""" 
Encode the input to base64 and return it. 
""" 
def encode_base64(convertable):
    return base64.b64encode(convertable)
    
""" 
Decode the input from base64 and return it. If unsuccesfull, 
return an empty string. 
""" 
def decode_base64(convertable):
    try:
        return base64.b64decode(convertable)
    except:
        return ''

""" 
Convert the input from integer to binary and return it. If unsuccesfull, 
return an empty string. 
""" 
def integer_to_binary(convertable):
    try:
        return bin(int(convertable))[2:].zfill(8)
    except:
        return ''

""" 
Convert the input from text to binary and return it. If unsuccesfull, 
return an empty string. 
""" 
def ascii_to_binary(convertable):
    try:
        return ''.join(format(ord(c), 'b').zfill(8) for c in convertable)
    except:
        return ''

""" 
Convert the input from binary to integer and return it. If unsuccesfull, 
return an empty string. 
""" 
def binary_to_int(convertable):
    try:
        return int(convertable, 2)
    except:
        return ''

""" 
Convert the input from binary to ascii text and return it. If unsuccesfull, 
return an empty string. 
""" 
def binary_to_ascii(convertable):
    result = ''
    try:
        for i in range(0, len(convertable), 8):
            result += binascii.unhexlify('%x' % int(convertable[i:i+8], 2))
        return result
    except:
        return ''
 
