# -*- coding: UTF-8 -*-
""" Convert variables from one type to another. """
from builtins import chr
import codecs
import base64
import binascii
import sys


ASCII_VALUE = '1'   # ascii
DECIMAL_VALUE = '2' # decimal
HEX_VALUE = '3'     # hex
BINARY_VALUE = '4'  # binary
BASE64_VALUE = '5'


class Conversion(object):
    """ Convert variable of some type to another type. """

    def __init__(self):
        self.default_return_value = ''


""" Ascii convertables """

class AsciiConversion(Conversion):
    """ Convert an ascii string to another type. """
    source_type_id = ASCII_VALUE 

    def __init__(self, convertable):
        super(AsciiConversion, self).__init__()
        self.convertable = convertable


class AsciiToDecimal(AsciiConversion):
    """
    Convert the input from ascii to decimal and return it. If unsuccesfull,
    return an empty string.
    """
    target_type_id = DECIMAL_VALUE
    
    def __init__(self, convertable):
        super(AsciiToDecimal, self).__init__(convertable)
        self.title = 'Ascii to decimal'
        
    def get_value(self):
        try:
            if sys.version_info >= (3, 0):
                return ord(self.convertable)
            else:
                return ord(self.convertable.decode('utf-8'))
        except TypeError:
            try:
                numbers = []
                for i in self.convertable:
                    numbers.append(ord(i))
                return numbers
            except TypeError:
                return self.default_return_value


class AsciiToHex(AsciiConversion):
    """ Convert an ascii variable to hex. """

    target_type_id = HEX_VALUE

    def __init__(self, convertable):
        super(AsciiToHex, self).__init__(convertable)
        self.title = 'Ascii to hex'

    def get_value(self):
        """
        Convert the input from ascii text to hex and return it. If unsuccesfull,
        return an empty string.
        """
        if sys.version_info >= (3, 0):
            self.convertable = self.convertable.encode('utf-8')
            return codecs.encode(self.convertable, 'hex').decode('utf-8')
        else:
            return binascii.hexlify(self.convertable)


class AsciiToBinary(AsciiConversion):
    """ Convert an ascii variable to binary. """

    target_type_id = BINARY_VALUE

    def __init__(self, convertable):
        super(AsciiToBinary, self).__init__(convertable)
        self.title = 'Ascii to binary'
        
    def get_value(self):
        """
        Convert the input from text to binary and return it. If unsuccesfull,
        return an empty string.
        """
        if sys.version_info >= (3, 0):
            return ''.join(format(ord(c), 'b').zfill(8) for c in self.convertable)
        else:
            return ''.join(format(ord(c), 'b').zfill(8) for c in self.convertable.decode('utf-8'))


class EncodeBase64(AsciiConversion):

    target_type_id = BASE64_VALUE

    def __init__(self, convertable):
        super(EncodeBase64, self).__init__(convertable)
        self.title = 'Encode base64'

    def get_value(self):
        """
        Encode the input to base64 and return it.
        """
        try:
            if sys.version_info >= (3, 0):
                return base64.b64encode(self.convertable.encode('utf-8')).decode('utf-8')
            else:
                return base64.b64encode(self.convertable)
        except AttributeError:
            return base64.b64encode(str(self.convertable))


class DecodeBase64(AsciiConversion):

    target_type_id = ASCII_VALUE

    def __init__(self, convertable):
        super(DecodeBase64, self).__init__(convertable)
        self.title = 'Decode base64'

    def get_value(self):
        """
        Decode the input from base64 and return it. If unsuccesfull,
        return an empty string.
        """
        if self.convertable:
            for _ in range(3):
                try:
                    return base64.b64decode(self.convertable).decode('ascii')
                except (TypeError, binascii.Error, ValueError):
                    self.convertable += '='
                except UnicodeDecodeError: # TODO Should this do "return ''"?
                    self.convertable += '='
        return self.default_return_value


""" Decimal convertables """

class DecimalConversion(Conversion):
    """ Convert a decimal variable to another type. """
    
    source_type_id = DECIMAL_VALUE
    
    def __init__(self, convertable):
        super(DecimalConversion, self).__init__()
        try:
            self.convertable = int(convertable)
        except ValueError:
            return self.default_return_value


class DecimalToAscii(DecimalConversion):
    """ Convert a decimal variable to ascii. """

    target_type_id = ASCII_VALUE 

    def __init__(self, convertable):
        super(DecimalToAscii, self).__init__(convertable)
        self.title = 'Decimal to ascii'

    def get_value(self):
        try:
            return chr(int(self.convertable))
        except (ValueError, AttributeError, OverflowError):
            return self.default_return_value


class DecimalToHex(DecimalConversion):
    """ Convert a decimal variable to hex. """

    target_type_id = HEX_VALUE

    def __init__(self, convertable):
        super(DecimalToHex, self).__init__(convertable)
        self.title = 'Decimal to hex'
        
    def get_value(self):
        try:
            return hex(int(self.convertable))[2:]
        except AttributeError:
            return self.default_return_value


class DecimalToBinary(DecimalConversion):
    """ Convert a decimal variable to binary. """

    target_type_id = BINARY_VALUE

    def __init__(self, convertable):
        super(DecimalToBinary, self).__init__(convertable)
        self.title = 'Decimal to binary'
        
    def get_value(self):
        #print self.convertable
        try:
            return '{0:08b}'.format(self.convertable)
        except AttributeError:
            return self.default_return_value


""" Hex convertables """

class HexConversion(Conversion):
    """ Convert a hex string to another type. """

    source_type_id = HEX_VALUE

    def __init__(self, convertable):
        super(HexConversion, self).__init__()
        self.convertable = convertable
        '''print(convertable)
        try:
            self.convertable = convertable
        except TypeError:
            self.convertable = None'''


class HexToAscii(HexConversion):
    """ Convert a hex string to ascii. """

    target_type_id = ASCII_VALUE

    def __init__(self, convertable):
        super(HexToAscii, self).__init__(convertable)
        self.title = 'Hex to ascii'

    def get_value(self):
        try:
            if len(self.convertable) % 2 != 0:
                self.convertable = '0' + self.convertable
            return chr(HexToDecimal(self.convertable).get_value())
        except (TypeError, ValueError, OverflowError):
            if len(self.convertable) % 2 != 0:
                self.convertable = '0' + self.convertable
            try:
                c = ''
                for i in range(0, len(self.convertable), 2):
                    c += chr(HexToDecimal(self.convertable[i:i+2]).get_value())
                return c
            except (TypeError, ValueError):
                return self.default_return_value
   
            return self.default_return_value


class HexToDecimal(HexConversion):
    """ Convert a hex string to decimal. """

    target_type_id = DECIMAL_VALUE

    def __init__(self, convertable):
        super(HexToDecimal, self).__init__(convertable)
        self.title = 'Hex to decimal'

    def get_value(self):
        try:
            return int(self.convertable, 16)
        except (TypeError, ValueError, AttributeError):
            return self.default_return_value


class HexToBinary(HexConversion):
    """ Convert a hex string to binary. """

    target_type_id = BINARY_VALUE

    def __init__(self, convertable):
        super(HexToBinary, self).__init__(convertable)
        self.title = 'Hex to binary'

    def get_value(self):
        try:
            return '{0:08b}'.format(int(self.convertable, 16))
        except (TypeError, ValueError):
            return self.default_return_value


""" Binary convertables """
class BinaryConversion(Conversion):
    """ Convert a binary number to another type. """
    source_type_id = BINARY_VALUE

    def __init__(self, convertable):
        super(BinaryConversion, self).__init__()
        binary_list_of_truths = [str(c) == '1' or str(c) == '0' for c in str(convertable)]
        if binary_list_of_truths and all(binary_list_of_truths):
            self.convertable = convertable
        else:
            self.convertable = self.default_return_value


class BinaryToAscii(BinaryConversion):
    """ Convert a binary number to ascii. """
    target_type_id = ASCII_VALUE

    def __init__(self, convertable):
        super(BinaryToAscii, self).__init__(convertable)
        self.title = 'Binary to ascii'

    def get_value(self):
        """
        Convert the input from binary to ascii text and return it. If unsuccesfull,
        return an empty string.
        """
        try:
            result = b''
            for i in range(0, len(self.convertable), 8):
                result += binascii.unhexlify('%x' % int(self.convertable[i:i+8], 2))
            return result.decode('ascii')
        except (ValueError, TypeError):
            return self.default_return_value


class BinaryToDecimal(BinaryConversion):
    """ Convert a binary number to decimal. """
    target_type_id = DECIMAL_VALUE

    def __init__(self, convertable):
        super(BinaryToDecimal, self).__init__(convertable)
        self.title = 'Binary to decimal'

    def get_value(self):
        try:
            return int(self.convertable, 2)
        except (ValueError, AttributeError):
            return self.default_return_value


class BinaryToHex(BinaryConversion):
    """ Convert a binary number to hex. """

    target_type_id = HEX_VALUE

    def __init__(self, convertable):
        super(BinaryToHex, self).__init__(convertable)
        self.title = 'Binary to hex'

    def get_value(self):
        try:
            if self.convertable:
                return int(self.convertable, 16)
            else:
                return self.default_return_value
        except ValueError:
            return self.default_return_value

