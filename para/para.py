#!/usr/bin/env python
import argparse
import logging
import sys
import ast
import inspect
import convert
import cipher

logger = logging.getLogger(__name__)
printoffset = 19

""" Calls a function received as a parameter and logs the result. """
def log_event(convertion_function, convertable, printable_text):
    formatstring = '{0: <' + str(printoffset) + '}'
    try:
        result = convertion_function(convertable)
    # Capture errors from functions which require wrong number of parameters
    except TypeError: 
        logger.debug('Failed to run function: ' + printable_text)
        return
    
    # If not Quiet mode: print the table
    if not logger.getEffectiveLevel() is 50:
        logevent = formatstring.format(printable_text) + ' | ' + str(result)
    if result:
        logger.critical(logevent)
    else:
        logger.info(logevent)
        
""" Calls log_event for each function in the convert module. """
def print_results(convertable):
    formatstring = '{0: <' + str(printoffset) + '}'
    logger.warn(formatstring.format('Action') + ' | ' + 'Result')
    logger.warn('-' * printoffset * 3)
    logevent = formatstring.format('User input ') + ' | ' + str(convertable)
    logger.info(logevent)
    
    # Get list of functions in the convert module and call them
    convert_functions = inspect.getmembers(convert, inspect.isfunction)
    for f in convert_functions:
        title = f[0].replace('_', ' ').capitalize()
        log_event(f[1], (convertable), title)
    log_event(cipher.rotate, (convertable), 'ROT13')

""" Initiates logging """
def set_logging(verbose, quiet):
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(message)s'.strip())
    ch.setFormatter(formatter)
    
    if verbose:
        logger.setLevel(logging.INFO)
    elif quiet:
        logger.setLevel(logging.CRITICAL)
    else:
        logger.setLevel(logging.WARN)
    
    logger.addHandler(ch)

""" Creates command-line interface and processes arguments. """
def process_arguments():
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
    args = parser.parse_args()
    
    if not args.convertable:
        if not sys.__stdin__.isatty():
            line = sys.__stdin__.readline().strip()
            args.convertable += str(ast.literal_eval('"' + line + '"'))
            args.convertable.strip()
        else:
            raise parser.error("error: too few arguments")
    
    set_logging(args.verbose, args.quiet)
    if args.rot:
        cipher.solve_rotation(args.convertable)
    else:
        print_results(args.convertable)
    logging.shutdown()

if __name__ == '__main__':
    process_arguments()
