"""py3fs_shell -- test cases to exercise new FS and shell utilities in Python3 Core API

we're actually addressing two things in the stdlib (``os.scandir()`` and ``subprocess.run()``), but we're
treating these as core because they're replacements for Py2 core items. See spec for scope notes.

Entry points in ``__main__.py``
"""

import os, subprocess
import io, pprint


def cwe73_os_scandir_sink():
    """shows how scandir can result in path traversal

    Provide the path to a *directory* to find the size of each file in it"""
    dir_to_scan = input("Enter path to scan: ")  # taint source
    for elem in os.scandir(dir_to_scan):  # CWEID 73
        # above is CWE-73 because elem will now have user-controlled path
        # SCRUB: can FP if the paths are not used to actually stat/read files (but otherwise why?)
        fstats = os.stat(elem)
        print("file '{}' is {} bytes".format(elem.name, fstats.st_size))


def cwe78_subprocess_run():
    """shows how run() can be used to OS command inject; similar to Popen/etc.

    Provide a command like ``ls``, because this will get executed!"""
    command = input("Enter command to run: ")  # taint source
    subprocess.run(command, shell=True)  # CWEID 78
    subprocess.run([command, '-l', '-h'], shell=True)  # CWEID 78
    subprocess.run([command, '-l'])  # SAFE! if shell is not set True, it checks to see if ``command`` is a file


def cwe73_subprocess_run():
    """shows how the cwd= attribute of run() can lead to path traversal"""
    path = input("Directory to list: ")  # taint source

    # cwd is the working directory a command is run in: path is tainted, so path traversal is possible
    # SCRUB: if the path is validated/whitelisted first, this can be FP
    subprocess.run(['ls', '-l'], cwd=path)  # CWEID 73
