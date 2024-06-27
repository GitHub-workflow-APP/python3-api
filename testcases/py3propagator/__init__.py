"""py3propagator - a test module that exercises new propagagors in the Python3 core API

see ``__main__.py`` for the application entry point
"""

import os, sys
import logging

logger = logging.getLogger(__name__)


def run_args_with_dict():
    """demo how a dict populated with either tainted keys or values can propagate that taint through the
    new .items() .keys() and .values() methods on ``dict``

    We are using os.system as a CWE-78 sink and sys.argv to make the point -- those are not new sources/sinks
    so this approach should isolate the propagators we're interested in
    """
    argkeys = dict()
    argvals = dict()
    count = 0

    for arg in sys.argv[1:]:   # sys.argv is tainted
        argkeys[arg] = len(arg)  # this is a little dumb, but... we propagate taint to the dictionary keys
        argvals[count] = arg     # this is _also_ a little dumb... we propagate taint to the dictionary values
        count += 1

    command_one = ' '.join(argkeys.keys())  # keys propagates through the assignment
    command_two = ' '.join(argvals.values())  # values propagates through the assignment

    os.system(command_one)  # CWEID 78
    os.system(command_two)  # CWEID 78

    command_three = ''
    for item in argkeys.items():  # taint propagates through the items() iterator
        command_three += item[0] + ' '  # items() returns (key, value) tuples, so item[0] is the tainted key
        os.system(command_three)  # CWEID 78

    return True


def run_args_with_bytestring():
    """demo how bytes() propagates tainted strings

    We are using os.system as a CWE-78 sink, and sys.argv to make the point -- see ``run_args_with_dict``
    for rationale"""

    commandstr = ' '.join(sys.argv[1:])  # join tainted args into tainted string
    commandbytes = bytes(commandstr)  # bytes constructor propagates taint

    # Below is a regression -- it should work without any changes, and keep working
    os.system(commandstr)  # CWEID 78

    # Here's the new thing -- taint needs to be tracked to bytes()
    return os.system(commandbytes)


def run_args_with_exception_from():
    """demo how ``raise Exception from`` propagates taint"""
    command = ' '.join(sys.argv[1:])  # taint pulled from argv source
    commandV = 'ls'

    # This is kind of a weird thing to demo, but I have seen things like this
    try:
        raise RuntimeError(command)  # because this is in a try, it propagates to the except scope
    except RuntimeError as e:
        try:
            raise ValueError(commandV) from e
        except ValueError as v:
            # commandV is the first of v.args, not tainted, no error
            logger.warning(msg=' '.join(v.args))

            # __context__ propagated 'e', so context.args[0], is ``command`` which is tainted
            # this makes log injection
            logger.warning(msg=' '.join(v.__context__.args))  # CWEID 117


def run_args_from_list_copy():
    """demo how list and bytearray have copy() methods that propagate taint"""
    arglist = sys.argv[1:]
    arglistcopy = arglist.copy()  # makes a *copy* of arglist, taint propagates

    argbytes = bytearray(' '.join(sys.argv[1:]), encoding='ascii')  # bytearray propagates taint
    argbytescopy = argbytes.copy()  # copy propagates!

    os.system(bytes(argbytescopy))  # CWEID 78
    return os.system(' '.join(arglistcopy))  # CWEID 78


def run_args_with_dict_comprehension():
    """demo how a comprehension still propagates; same idea of ``run_args_with_dict`` except we do a silly comprehension
    and only include .keys()
    """
    argkeys = dict()

    for arg in sys.argv[1:]:   # sys.argv is tainted
        argkeys[arg] = len(arg)  # this is a little dumb, but... we propagate taint to the dictionary keys

    argmapped = {k: v+1 for k, v in argkeys}  # the keys are propagated through the comprehension
    command_one = ' '.join(argmapped.keys())  # keys propagates through the assignment

    os.system(command_one)  # CWEID 78

    return True

