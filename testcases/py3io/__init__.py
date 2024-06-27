"""py3_io - a test module that exercises new propagagors in the Python3 core API

see ``__main__.py`` for the application entry point
"""

import io, os


def run_input_with_stringio():
    # Under Py2, the line below would be unsafe because the input is evaluated
    # e.g. entering 'exit()' at the prompt would cause the python app to exit
    # In Py3 it is *safe* and is only a taint source
    cmd = input("Enter a command string to run: ")  # taint source
    cmdio = io.StringIO(cmd)  # cmdio will propagate taint
    cmdstr = ''

    lastchar = cmdio.read(1)  # lastchar is tainted because we're reading from a TextIOBase obj built on a tainted str
    while lastchar is not None and len(lastchar):
        cmdstr += lastchar
        lastchar = cmdio.read(1)  # taint continues to propagate

    os.system(cmdstr)

    cmdiostr = io.StringIO('')
    cmdiostr.write(cmdstr)  # propagates tainted cmdstr by writing it to cmdiostr

    # TextIOBase objects (StringIO and BytesIO) seek to 0 when reading after write
    os.system(cmdiostr.read())  # CWEID 78


def run_input_with_bytesio():
    # Under Py2, the line below would be unsafe because the input is evaluated
    # e.g. entering 'exit()' at the prompt would cause the python app to exit
    # In Py3 it is *safe* and is only a taint source
    cmd = input("Enter a command string to run: ")  # taint source
    cmdio = io.BytesIO(bytes(cmd, encoding='ascii'))  # cmdio will propagate taint, as does bytes()
    cmdstr = bytearray(b'')

    lastchar = cmdio.read(1)  # lastchar is tainted because we're reading from a TextIOBase obj built on a tainted str
    while lastchar != b' ' and lastchar is not None and len(lastchar):
        cmdstr.extend(lastchar)
        lastchar = cmdio.read(1)  # taint continues to propagate

    os.system(bytes(cmdstr))  # CWEID 78

    cmdiostr = io.BytesIO(b'')
    cmdiostr.write(bytes(cmdstr))  # propagates tainted cmdstr by writing it to cmdiostr

    # TextIOBase objects (StringIO and BytesIO) seek to 0 when reading after write
    os.system(cmdiostr.read())  # CWEID 78


def run_input_with_open():
    with open(input("enter file name:"), 'r') as cmdfile:  # cmdfile has tainted contents
        for cmdline in cmdfile:
            os.system(cmdline)  # CWEID 78


def _opener(file, flags):
    """the opener for ``opener_control_flow()`` below

    this changes the file name and then opens _that_ file. We should be able to see
    this in call stacks when tracing flow
    """

    return os.open(file+'.bak', flags)


def opener_control_flow():
    """testing control flow for custom opener"""

    with open(input("enter file name:"), 'r', opener=_opener) as cmdfile:  # cmdfile has tainted contents
        for cmdline in cmdfile:
            os.system(cmdline)  # CWEID 78
