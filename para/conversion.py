# -*- coding: UTF-8 -*-
""" Convert variables from one type to another. """
from builtins import chr
import base64
import binascii
import sys
import string


ASCII_VALUE = '1'    # ascii
DECIMAL_VALUE = '2'  # decimal
HEX_VALUE = '3'      # hex
BINARY_VALUE = '4'   # binary
BASE64_VALUE = '5'


class Conversion(object):
    """ Convert variable of some type to another type. """

    def __init__(self, convertable=''):
        self.default_return_value = ''
        self.convertable = convertable

    def parse(self, result):
        if sys.version_info < (3, 0):
            return result.encode('utf-8')
        else:
            return result


""" Ascii convertables """


class AsciiConversion(Conversion):
    """ Convert an ascii string to another type. """
    source_type_id = ASCII_VALUE

    def __init__(self, convertable):
        super(AsciiConversion, self).__init__(convertable)


class AsciiToDecimal(AsciiConversion):
    """
    Convert the input from ascii to decimal and return it.
    If unsuccesfull, return an empty string.
    """
    target_type_id = DECIMAL_VALUE

    def __init__(self, convertable):
        super(AsciiToDecimal, self).__init__(convertable)
        self.title = 'Ascii to decimal'

    def get_value(self):
        try:
            return ord(self.parse(self.convertable))
        except (TypeError, AttributeError):
            try:
                ret = []
                for i in self.convertable:
                    ret.append(ord(i))
            except TypeError:
                ret = self.default_return_value
        if ret:
            return ret
        else:
            return self.default_return_value


class AsciiToHex(AsciiConversion):
    """ Convert an ascii variable to hex. """
    target_type_id = HEX_VALUE

    def __init__(self, convertable):
        super(AsciiToHex, self).__init__(convertable)
        self.title = 'Ascii to hex'

    def get_value(self):
        """
        Convert the input from ascii text to hex and return it.
        If unsuccesfull, return an empty string.
        """
        try:
            return hex(ord(self.parse(self.convertable)))[2:]
        except TypeError:
            if sys.version_info >= (3, 0):
                #self.convertable = self.convertable.encode('utf-8')
                return binascii.hexlify(self.convertable).decode('utf-8')
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
        Convert the input from text to binary and return it.
        If unsuccesfull, return an empty string.
        """
        if sys.version_info >= (3, 0):
            return ''.join(format(ord(c), 'b').zfill(8)
                           for c in self.convertable)
        else:
            return ''.join(format(ord(c), 'b').zfill(8)
                           for c in self.convertable.decode('utf-8'))


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
                self.convertable = self.convertable.encode('utf-8')
                return base64.b64encode(self.convertable).decode('utf-8')
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
                    return base64.b64decode(self.convertable).decode('utf-8')
                except (TypeError, binascii.Error, ValueError):
                    self.convertable += '='
                except UnicodeDecodeError:
                    # TODO Should this do "return ''"?
                    self.convertable += '='
        return self.default_return_value


""" Decimal convertables """


class DecimalConversion(Conversion):
    """ Convert a decimal variable to another type. """
    source_type_id = DECIMAL_VALUE

    def __init__(self, convertable):
        super(DecimalConversion, self).__init__()
        try:
            if len(convertable.split()) > 1:
                self.convertable = [int(x) for x in convertable.split()]
            else:
                self.convertable = int(convertable)
        except (ValueError, AttributeError):
            return self.default_return_value


class DecimalToAscii(DecimalConversion):
    """ Convert a decimal variable to ascii. """
    target_type_id = ASCII_VALUE

    def __init__(self, convertable):
        super(DecimalToAscii, self).__init__(convertable)
        self.title = 'Decimal to ascii'

    def get_value(self):
        if type(self.convertable) == list:
            result = []
            try:
                for value in self.convertable:
                    result.append(chr(int(value)))
            except (ValueError, AttributeError):
                return self.default_return_value
            return ''.join(result)
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
        if type(self.convertable) == list:
            result = []
            try:
                for value in self.convertable:
                    result.append(hex(int(value))[2:])
            except AttributeError:
                return self.default_return_value
            return ''.join(result)
        try:
            return hex(int(self.convertable))[2:]
        except (AttributeError, ValueError):
            return self.default_return_value


class DecimalToBinary(DecimalConversion):
    """ Convert a decimal variable to binary. """
    target_type_id = BINARY_VALUE

    def __init__(self, convertable):
        super(DecimalToBinary, self).__init__(convertable)
        self.title = 'Decimal to binary'

    def get_value(self):
        if type(self.convertable) == list:
            result = []
            try:
                for value in self.convertable:
                    result.append('{0:08b}'.format(value))
            except AttributeError:
                return self.default_return_value
            return ''.join(result)
        try:
            return '{0:08b}'.format(self.convertable)
        except (AttributeError, ValueError):
            return self.default_return_value


""" Hex convertables """


class HexConversion(Conversion):
    """ Convert a hex string to another type. """
    source_type_id = HEX_VALUE

    def __init__(self, convertable):
        super(HexConversion, self).__init__()
        if type(convertable) == list:
            self.convertable = convertable
        else:
            self.convertable = convertable.split()


class HexToAscii(HexConversion):
    """ Convert a hex string to ascii. """
    target_type_id = ASCII_VALUE

    def __init__(self, convertable):
        super(HexToAscii, self).__init__(convertable)
        self.title = 'Hex to ascii'

    def get_value(self):
        try:
            if len(self.convertable[0]) <= 2:
                result = ''
                for value in self.convertable:
                    result += chr(HexToDecimal(value).get_value())
                return self.parse(result)
            else:
                raise TypeError
        except (ValueError, TypeError, OverflowError):
            try:
                if len(self.convertable) % 2 != 0:
                    self.convertable = '0' + self.convertable
                c = ''
                for i in range(0, len(self.convertable), 2):
                    c += chr(HexToDecimal(
                             self.convertable[i:i+2]).get_value())
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
        result = []
        for value in self.convertable:
            try:
                result.append(int(value, 16))
            except (TypeError, ValueError, AttributeError):
                return self.default_return_value
        if not result:
            return self.default_return_value
        elif len(result) == 1:
            return result[0]
        else:
            return result


class HexToBinary(HexConversion):
    """ Convert a hex string to binary. """
    target_type_id = BINARY_VALUE

    def __init__(self, convertable):
        super(HexToBinary, self).__init__(convertable)
        self.title = 'Hex to binary'

    def get_value(self):
        try:
            result = []
            for value in self.convertable:
                result.append('{0:08b}'.format(int(value, 16)))
            if not result:
                return self.default_return_value
            elif len(result) == 1:
                return result[0]
            else:
                return ' '.join(result)
        except (TypeError, ValueError):
            return self.default_return_value


""" Binary convertables """


class BinaryConversion(Conversion):
    """ Convert a binary number to another type. """
    source_type_id = BINARY_VALUE

    def __init__(self, convertable):
        super(BinaryConversion, self).__init__()
        binary_list_of_truths = [
            str(c) == '1' or str(c) == '0' for c in str(convertable)]
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
        Convert the input from binary to ascii text and return it.
        If unsuccesfull, return an empty string.
        """
        try:
            while len(self.convertable) < 8:
                self.convertable = '0' + self.convertable
            result = ''
            for i in range(0, len(self.convertable), 8):
                result += chr(int(self.convertable[i:i+8], 2))
            if all([str(c) in string.printable for c in result]):
                return result
            else:
                return self.default_return_value
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
                return hex(int(self.convertable, 2))[2:]
            else:
                return self.default_return_value
        except ValueError:
            return self.default_return_value
