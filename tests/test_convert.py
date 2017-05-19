# -*- coding: UTF-8 -*-
""" Test cases against convert functions. """
import para.conversion as convert
import unittest


class TestConvert(unittest.TestCase):

    def test_decimal_to_ascii(self):
        self.assertEqual(convert.DecimalToAscii('123').get_value(), '{')

    def test_decimal_to_ascii(self):
        self.assertEqual(convert.DecimalToAscii('123 123').get_value(), '{{')

    def test_decimal_to_ascii_fail(self):
        self.assertEqual(convert.DecimalToAscii('asd').get_value(), '')

    def test_ascii_to_decimal(self):
        self.assertEqual(convert.AsciiToDecimal('{').get_value(), 123)

    """
    def test_ascii_to_decimal_fail(self):
        print convert.AsciiToDecimal(1).get_value()
        self.assertEqual(convert.AsciiToDecimal(1).get_value(), '')
    """

    def test_decimal_to_hex(self):
        self.assertEqual(convert.DecimalToHex('123').get_value(), '7b')

    def test_decimal_to_hex_fail(self):
        self.assertEqual(convert.DecimalToHex('asd').get_value(), '')

    def test_hex_to_decimal(self):
        self.assertEqual(convert.HexToDecimal('7b').get_value(), 123)

    def test_hex_to_binary(self):
        self.assertEqual(convert.HexToBinary('7b').get_value(), '01111011')

    def test_binary_to_hex(self):
        self.assertEqual(convert.BinaryToHex('01111011').get_value(), '7b')

    def test_binary_to_hex_failure(self):
        self.assertEqual(convert.BinaryToHex('ää').get_value(), '')

    def test_hex_to_decimal_fail(self):
        self.assertEqual(convert.HexToDecimal('sk').get_value(), '')

    def test_ascii_to_hex(self):
        self.assertEqual(convert.AsciiToHex('123').get_value(), '313233')

    """
    def test_ascii_to_hex_fail(self):
        self.assertEqual(convert.AsciiToHex(123).get_value(), '')
    """

    def test_hex_to_ascii(self):
        self.assertEqual(convert.HexToAscii('7b').get_value(), '{')

    def test_hex_list_to_ascii(self):
        self.assertEqual(
            convert.HexToAscii('de ad be ef').get_value(), u'Þ­¾ï')

    def test_hex_string_to_ascii(self):
        self.assertEqual(convert.HexToAscii('666c6167').get_value(), 'flag')

    def test_hex_to_ascii_fail(self):
        self.assertEqual(convert.HexToAscii('sk').get_value(), '')

    def test_encode_base64(self):
        self.assertEqual(convert.EncodeBase64('123').get_value(), 'MTIz')

    def test_decode_base64(self):
        self.assertEqual(convert.DecodeBase64('MTIz').get_value(), '123')

    def test_decode_base64_fail(self):
        self.assertEqual(convert.DecodeBase64('92438y7').get_value(), '')

    def test_decimal_to_binary(self):
        self.assertEqual(
            convert.DecimalToBinary('123').get_value(), '01111011')

    def test_decimal_to_binary_fail(self):
        self.assertEqual(convert.DecimalToBinary('asd').get_value(), '')

    def test_ascii_to_binary(self):
        self.assertEqual(
            convert.AsciiToBinary('123').get_value(),
            '001100010011001000110011')

    """
    def test_ascii_to_binary_fail(self):
        self.assertEqual(convert.AsciiToBinary(123).get_value(), '')
    """

    def test_binary_to_decimal(self):
        self.assertEqual(convert.BinaryToDecimal('01111011').get_value(), 123)

    def test_binary_to_decimal_fail(self):
        self.assertEqual(convert.BinaryToDecimal('234').get_value(), '')

    def test_binary_to_ascii(self):
        self.assertEqual(
            convert.BinaryToAscii('001100010011001000110011').get_value(),
            '123')

    def test_binary_to_ascii_fail(self):
        self.assertEqual(convert.BinaryToAscii('2345').get_value(), '')

    """
    def test_rotation_simple(self):
        self.assertEqual(cipher.rotate('T2st1ngR0tat10n'), '6fFGeAt4dGnGedA')
    """

    def test_chars(self):
        self.assertEqual(
            convert.AsciiToDecimal('ä'.encode('utf-8')).get_value(), '228')

    def test_chars(self):
        self.assertEqual(convert.DecimalToAscii('228').get_value(), 'ä')


if __name__ == '__main__':
    unittest.main()
