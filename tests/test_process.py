# -*- coding: UTF-8 -*-
""" Test the Para module. """
import para.para as para
import sys
import unittest
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

try:
    if os.name == 'posix' and sys.version_info[0] < 3:
        import subprocess32 as subprocess
    else:
        import subprocess
except:
    import subprocess


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
        result = parse('Action              | Result\n' + \
                 '---------------------------------------------------------\n' + \
                 'Ascii to binary     | 001100010011001000110011\n' + \
                 'Ascii to decimal    | [49, 50, 51]\n' + \
                 'Ascii to hex        | 313233\n' + \
                 'Encode base64       | MTIz\n' + \
                 'Decimal to ascii    | {\n' + \
                 'Decimal to binary   | 01111011\n' +  \
                 'Decimal to hex      | 7b\n' + \
                 'Hex to ascii        | ģ\n' + \
                 'Hex to binary       | 100100011\n' + \
                 'Hex to decimal      | 291')
        out = StringIO()
        para.process_arguments(out, ['123'])
        my_result = out.getvalue().strip()
        self.assertMultiLineEqual(my_result, result)

    def test_verbosity(self):
        """ Test para with a basic input using verbose mode. """
        result = parse('Action              | Result\n' + \
                 '---------------------------------------------------------\n' + \
                 'User input          | 123\n' + \
                 'Ascii to binary     | 001100010011001000110011\n' + \
                 'Ascii to decimal    | [49, 50, 51]\n' + \
                 'Ascii to hex        | 313233\n' + \
                 'Decode base64       | \n' + \
                 'Encode base64       | MTIz\n' + \
                 'Binary to ascii     | \n' + \
                 'Binary to decimal   | \n' + \
                 'Binary to hex       | \n' + \
                 'Decimal to ascii    | {\n' + \
                 'Decimal to binary   | 01111011\n' + \
                 'Decimal to hex      | 7b\n' + \
                 'Hex to ascii        | ģ\n' + \
                 'Hex to binary       | 100100011\n' + \
                 'Hex to decimal      | 291')
        out = StringIO()
        para.process_arguments(out, ['-v', '123'])
        my_result = out.getvalue().strip()
        self.assertMultiLineEqual(my_result, result)

    def test_quiet(self):
        """ Test para with a basic input using quiet mode. """
        result = parse('001100010011001000110011\n[49, 50, 51]\n' + \
                 '313233\nMTIz\n{\n01111011\n7b\nģ\n100100011\n291')
        out = StringIO()
        para.process_arguments(out, ['-q', '123'])
        my_result = out.getvalue().strip()
        self.assertMultiLineEqual(my_result, result)


    def test_quiet_single_value(self):
        """ Test para with a basic input using quiet mode. """
        result = '{'
        out = StringIO()
        para.process_arguments(out, ['-q', '-s', '2', '-t', '1', '123'])
        my_result = out.getvalue().strip()
        self.assertMultiLineEqual(my_result, result)


if __name__ == '__main__':
    unittest.main()

