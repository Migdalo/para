#!/usr/bin/env python
"""
Para is a conversion tool that converts user input to hex, ascii,
decimal, base64, binary and ROT13.
"""
import argparse
import logging
import sys
import ast
import inspect

# For python 2 + python 3 compatibility
try:
    import convert
except ImportError:
    import para.convert as convert
try:
    import cipher
except ImportError:
    import para.cipher as cipher

LOGGER = logging.getLogger(__name__)
PRINT_OFFSET = 19

def log_event(convertion_function, convertable, printable_text):
    """ Call a function received as a parameter and log the result. """
    formatstring = '{0: <' + str(PRINT_OFFSET) + '}'
    try:
        result = convertion_function(convertable)
    except TypeError:
        # Capture errors from functions which require wrong number of parameters
        LOGGER.debug('Failed to run function: ' + printable_text)
        return

    if LOGGER.getEffectiveLevel() is not 50:
        # If not Quiet mode: print the table
        logevent = formatstring.format(printable_text) + ' | ' + str(result)
    else:
        logevent = str(result)

    if result:
        LOGGER.critical(logevent)
    else:
        LOGGER.info(logevent)

def print_results(convertable):
    """Call log_event for each function in the convert module."""
    formatstring = '{0: <' + str(PRINT_OFFSET) + '}'
    LOGGER.warning(formatstring.format('Action') + ' | ' + 'Result')
    LOGGER.warning('-' * PRINT_OFFSET * 3)
    logevent = formatstring.format('User input ') + ' | ' + str(convertable)
    LOGGER.info(logevent)

    # Get list of functions in the convert module and call them
    convert_functions = inspect.getmembers(convert, inspect.isfunction)
    for func in convert_functions:
        title = func[0].replace('_', ' ').capitalize()
        log_event(func[1], (convertable), title)
    log_event(cipher.rotate, (convertable), 'ROT13')

def set_logging(verbose, quiet, out):
    """ Initiate logging """
    stream_handler = logging.StreamHandler(out)
    formatter = logging.Formatter('%(message)s'.strip())
    stream_handler.setFormatter(formatter)

    if verbose:
        LOGGER.setLevel(logging.INFO)
    elif quiet:
        LOGGER.setLevel(logging.CRITICAL)
    else:
        LOGGER.setLevel(logging.WARNING)

    LOGGER.addHandler(stream_handler)

def process_arguments(out=sys.stdout, test_args=None):
    """ Create command-line interface and process arguments. """
    parser = argparse.ArgumentParser( \
        description='Converts strings and numbers to other types.',\
        epilog='Author: Migdalo (https://github.com/Migdalo)')
    parser.add_argument('convertable', nargs='?', default='', \
        help='String or number you want to convert.')
    parser.add_argument('-r', '--rot', action='store_true', \
        help='Print more rotation cipher results.')
    verbosity_group = parser.add_mutually_exclusive_group()
    verbosity_group.add_argument('-v', '--verbose', action='store_true', \
        help='Use verbose mode.')
    verbosity_group.add_argument('-q', '--quiet', action='store_true', \
        help='Use quiet mode.')

    if test_args:
        args = parser.parse_args(test_args)
    else:
        args = parser.parse_args()
        if not args.convertable:
            if not sys.__stdin__.isatty():
                line = sys.__stdin__.readline().strip()
                args.convertable += str(ast.literal_eval('"' + line + '"'))
                args.convertable.strip()
            else:
                raise parser.error("error: too few arguments")

    set_logging(args.verbose, args.quiet, out)
    if args.rot:
        cipher.solve_rotation(args.convertable)
    else:
        print_results(args.convertable)
    logging.shutdown()

if __name__ == '__main__':
    process_arguments()
