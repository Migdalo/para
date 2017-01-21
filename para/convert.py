"""
Convert module includes functions to convert a variable type to another.
"""
import base64
import binascii
import codecs

def decimal_to_ascii(convertable):
    """
    Convert the input from decimal to ascii text and return it. If unsuccesfull,
    return an empty string.
    """
    try:
        return chr(int(convertable))
    except (ValueError,  OverflowError):
        return ''

def ascii_to_decimal(convertable):
    """
    Convert the input from ascii to decimal and return it. If unsuccesfull,
    return an empty string.
    """
    try:
        return ord(convertable)
    except TypeError:
        try:
            numbers = []
            for i in convertable:
                numbers.append(ord(i))
            return numbers
        except TypeError:
            return ''

def decimal_to_hex(convertable):
    """
    Convert the input from decimal to hex and return it. If unsuccesfull,
    return an empty string.
    """
    try:
        return hex(int(convertable))[2:]
    except ValueError:
        return ''

def hex_to_decimal(convertable):
    """
    Convert the input from hex to decimal and return it. If unsuccesfull,
    return an empty string.
    """
    try:
        return int(convertable, 16)
    except ValueError:
        return ''

def ascii_to_hex(convertable):
    """
    Convert the input from ascii text to hex and return it. If unsuccesfull,
    return an empty string.
    """
    try:
        convertable = convertable.encode('ascii')
        return codecs.encode(convertable, 'hex').decode('ascii')
    except (ValueError, AttributeError):
        return ''

def hex_to_ascii(convertable):
    """
    Convert the input from hex to ascii text and return it. If unsuccesfull,
    return an empty string.
    """
    try:
        return codecs.decode(convertable, 'hex').decode('ascii')
    except (TypeError, binascii.Error):
        return ''

def encode_base64(convertable):
    """
    Encode the input to base64 and return it.
    """
    try:
        return base64.b64encode(convertable.encode()).decode()
    except AttributeError:
        return base64.b64encode(str(convertable))

def decode_base64(convertable):
    """
    Decode the input from base64 and return it. If unsuccesfull,
    return an empty string.
    """
    if convertable and isinstance(convertable, type('str')):
        for i in range(3):
            try:
                return base64.b64decode(convertable).decode('ascii')
            except (TypeError, binascii.Error):
                convertable += '='
            except UnicodeDecodeError: # TODO Should this do "return ''"?
                convertable += '='
    return ''

def decimal_to_binary(convertable):
    """
    Convert the input from decimal to binary and return it. If unsuccesfull,
    return an empty string.
    """
    try:
        return bin(int(convertable))[2:].zfill(8)
    except ValueError:
        return ''

def ascii_to_binary(convertable):
    """
    Convert the input from text to binary and return it. If unsuccesfull,
    return an empty string.
    """
    try:
        return ''.join(format(ord(c), 'b').zfill(8) for c in convertable)
    except TypeError:
        return ''

def binary_to_decimal(convertable):
    """
    Convert the input from binary to decimal and return it. If unsuccesfull,
    return an empty string.
    """
    try:
        return int(convertable, 2)
    except ValueError:
        return ''

def binary_to_ascii(convertable):
    """
    Convert the input from binary to ascii text and return it. If unsuccesfull,
    return an empty string.
    """
    result = b''
    try:
        for i in range(0, len(convertable), 8):
            result += binascii.unhexlify('%x' % int(convertable[i:i+8], 2))
        return result.decode('ascii')
    except ValueError:
        return ''
