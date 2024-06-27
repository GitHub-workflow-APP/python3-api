"""py3orderddict is an example testcase to exercise OrderedDict as a propagator

Essentially, we should treat OrderedDict collections as dict() objects; we use CWEID 78
with a well-established sink (``os.system()``) for these tests

entry points in __main__.py
"""

import os, collections, sys


def cwe78_with_ordered_dict_from_argv():
    ordered_args = collections.OrderedDict([('one', None),('two', None),('three', None)])
    i = 1
    for key in ordered_args:
        try:
            ordered_args[key] = sys.argv[i]  # taint sourced from sys.argv ends up in the OrderedDict
        except IndexError as e:
            ordered_args[key] = ''  # if there aren't enoug args, that's ok
        i += 1

    arg_string = ' '.join(ordered_args.values())  # taint propagates through .values(), just like a dict
    os.system(arg_string)   # CWEID 78


def cwe78_with_ordered_dict_keys_from_input():
    ordered_args = collections.OrderedDict()

    # collect tainted keys
    ordered_args[input("Enter command to execute: ")] = 'ls'
    ordered_args[input("Enter a parameter: ")] = '-l'
    ordered_args[input("Enter another parameter: ")] = '-h'

    arg_string = ' '.join(ordered_args)  # tainted keys (only!) propagate through
    os.system(arg_string)  # CWEID 78

    arg_string = ' '.join(ordered_args.values())  # values weren't tainted!
    os.system(arg_string)  # SAFE - since values never were tainted, there's no flaw here
