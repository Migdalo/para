# -*- coding: UTF-8 -*-
""" Test the Para module. """
import para.para as para
import sys
import unittest
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


if sys.version_info >= (3, 0):
    def parse(x):
        return x
else:
    def parse(x):
        return x.decode('utf-8')


class TestPara(unittest.TestCase):
    """ Test process_arguments() function. """

    def test_decimal_input(self):
        """ Test para with a basic input. """
        result = parse('Action              | Result\n' +
                       '-' * para.PRINT_OFFSET * 3 + '\n' +
                       'Ascii to binary     | 001100010011001000110011\n' +
                       'Ascii to decimal    | [49, 50, 51]\n' +
                       'Ascii to hex        | 313233\n' +
                       'Encode base64       | MTIz\n' +
                       'Decimal to ascii    | {\n' +
                       'Decimal to binary   | 01111011\n' +
                       'Decimal to hex      | 7b\n' +
                       'Hex to binary       | 100100011\n' +
                       'Hex to decimal      | 291')
        out = StringIO()
        para.process_arguments(out, test_args=['123'])
        my_result = out.getvalue().strip()
        self.assertMultiLineEqual(my_result, result)

    def test_verbosity(self):
        """ Test para with a basic input using verbose mode. """
        result = parse('Action              | Result\n' +
                       '-' * para.PRINT_OFFSET * 3 + '\n' +
                       'User input          | 123\n' +
                       'Ascii to binary     | 001100010011001000110011\n' +
                       'Ascii to decimal    | [49, 50, 51]\n' +
                       'Ascii to hex        | 313233\n' +
                       'Decode base64       | \n' +
                       'Encode base64       | MTIz\n' +
                       'Binary to ascii     | \n' +
                       'Binary to decimal   | \n' +
                       'Binary to hex       | \n' +
                       'Decimal to ascii    | {\n' +
                       'Decimal to binary   | 01111011\n' +
                       'Decimal to hex      | 7b\n' +
                       'Hex to ascii        | \n' +
                       'Hex to binary       | 100100011\n' +
                       'Hex to decimal      | 291')
        out = StringIO()
        para.process_arguments(out, test_args=['-v', '123'])
        my_result = out.getvalue().strip()
        self.assertMultiLineEqual(my_result, result)

    def test_quiet(self):
        """ Test para with a basic input using quiet mode. """
        result = parse('001100010011001000110011\n[49, 50, 51]\n313233' +
                       '\nMTIz\n{\n01111011\n7b\n100100011\n291')
        out = StringIO()
        para.process_arguments(out, test_args=['-q', '123'])
        my_result = out.getvalue().strip()
        self.assertMultiLineEqual(my_result, result)

    def test_quiet_single_value(self):
        """ Test para with a basic input using quiet mode. """
        result = '{'
        out = StringIO()
        para.process_arguments(
            out, test_args=['-q', '-s', '2', '-t', '1', '123'])
        my_result = out.getvalue().strip()
        self.assertMultiLineEqual(my_result, result)

    def test_no_value(self):
        """ Test para without giving any input. """
        out = StringIO()
        with self.assertRaises(SystemExit):
            para.process_arguments(out, test_args=[''])

    def test_list_value(self):
        """ Test para with a list input using quiet mode. """
        result = parse('001100010011000100110001001000000011000100110' +
                       '00100110001\n[49, 49, 49, 32, 49, 49, 49]\n' +
                       '31313120313131\nMTExIDExMQ==\noo\n' +
                       '0110111101101111\n6f6f\n' +
                       '100010001 100010001\n[273, 273]')
        out = StringIO()
        para.process_arguments(out, test_args=['-q', '111 111'])
        my_result = out.getvalue().strip()
        self.assertMultiLineEqual(my_result, result)

    def test_value_from_stdin(self):
        """ Test para by giving it input through stdin. """
        result = parse('Action              | Result\n' +
                       '-' * para.PRINT_OFFSET * 3 + '\n' +
                       'Ascii to binary     | 001100010011001000110011\n' +
                       'Ascii to decimal    | [49, 50, 51]\n' +
                       'Ascii to hex        | 313233\n' +
                       'Encode base64       | MTIz\n' +
                       'Decimal to ascii    | {\n' +
                       'Decimal to binary   | 01111011\n' +
                       'Decimal to hex      | 7b\n' +
                       'Hex to binary       | 100100011\n' +
                       'Hex to decimal      | 291')
        out = StringIO()
        instream = StringIO('123')
        para.process_arguments(out, instream)
        my_result = out.getvalue().strip()
        self.assertMultiLineEqual(my_result, result)

    def test_stdin_null_byte(self):
        """ Test para with input containing a null byte. """
        out = StringIO()
        instream = StringIO('\0')
        with self.assertRaises(SystemExit):
            para.process_arguments(out, instream)


if __name__ == '__main__':
    unittest.main()
