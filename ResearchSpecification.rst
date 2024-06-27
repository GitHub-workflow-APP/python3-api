#########################
Python3 API specification
#########################

:Authors:
	Darren Meyer <dmeyer@veracode.com>

.. contents::


:Targets:
	Python3 3.5.5  --  main targetted version

.. _builtin_functions: python3-builtin_functions.txt
.. _builtin_datatypes: python3-builtin_datatypes.txt


Scope
==============================================================================

This research targets Python 3.5; where it makes sense, the specification tries to "work" in a way that's compatible with everything from 3.2-3.6, but that's not always possible


Notable out-of-scope items
------------------------------------------------------------------------------

* Python 3.6's "f" strings (e.g. ``f"hello {name(current_user)}"``) seem like they have a lot of potential for abuse, but modeling them would be very difficult in the Simple Scanner, so they're out of scope

* `memoryview objects`_, while interesting, are rarely used directly and would be a lot of work to support, so they're out of scope. That means the ``memoryview()`` builtin is also out of scope


.. _memoryview objects: https://docs.python.org/3.5/library/stdtypes.html#typememoryview
 


Core API
==============================================================================

See the `builtin function list`_ and `builtin datatype list`_.

.. _builtin function list: builtin_functions_
.. _builtin datatype list: builtin_datatypes_


This is a list of changes to the Python3 core API that our scanner or pacakage handler might need to be aware of. It generally doesn't include changes to the stdlib -- there are a couple of exceptions for things that have moved from core to stdlib or things likely to see such heavy use that we can think of them as "core".


* ``print()`` is now a function. This should already be supported because it's available in 2.x through ``from __future__ import print_function``

* New **propagators**: ``dict.keys(), dict.items(), dict.values()`` -- these return iterators, that contain a portion of the data in the ``dict`` object. They can be treated as lists in most circumstances

* ``range()`` now works like py2's ``xrange()`` -- that is, it returns a *generator* instead of *list*. Which means things like you can't use slices. I'm not sure whether we care for scan purposes or not

* ``StringIO`` and ``cStringIO`` are gone, that functionality is now in ``io.StringIO`` and ``io.BytesIO``. We need to make sure we map the sources/sinks appropriately

* Annotations can be applied to parameters and return values (`PEP 3107 <https://www.python.org/dev/peps/pep-3107/#parameters>`_). They use a different syntax than decorators, which alters parsing. The annotations can be any object, and are available in the function's ``__annotations__`` mapping -- we need to make sure we can follow control/data flow there

* The ``nonlocal`` scope keyword allows a variable to reference an outer scope. Similar to ``global``, but only one scope-level up. 

* Unpacking lists and other iterables has additional syntax:
	* ``a, *b = list(1, 2, 3, 4, 5)`` -> ``a == 1, b = [2, 3, 4, 5]``
	* ``a, *b, c = list(1, 2, 3, 4, 5)`` -> ``a == 1, b = [2, 3, 4], c == 5``
	* ``*a, b = list(1, 2, 3, 4, 5)`` -> ``a == [1, 2, 3, 4], b = 5``

* In addition to list comprehensions, there are now `dict and set comprehensions`_

* List comprehensions also work a little differently:
	* ``[x for x in (item1, item2)]`` (note the parens now required)
	* The control variable (``x`` above) is no longer accessible outside of the comprehension

* Ellipsis notation (``...``) can be used outside of range operators, such as in array slices. Parser change, but shouldn't impact our simplistic scans

* Byte strings are a new syntax:
	* ``bytes(str)`` or ``b"literal`` return a ``bytes`` object. In most cases, we can think of this as a ``str`` for modeling and flow purposes. It propagates strings

* Raise exceptions with context: ``raise Exception from prior_exception`` is possible. Parser and propagation awareness (info from prior_exception is propagated to Exception)

* Metaclass syntax changed: ``class C(metaclass=M)``; parser awareness only

* There is no ``exec`` keyword, but the unsafe ``exec()`` function remains. Parser awareness.

* A number of modules in the stdlib were renamed or reorgnized, see `Python3.0-3.5_changes.rst`_ for details. I'm considering making those mappings to be out of scope unless the changes are needed to make something else pass

* ``str.format()`` for formating strings; we should already support this as it was available in 2.6. In 3.x it's not available on the new ``bytes`` style strings, only on ``str`` (unicode). Strings with tainted components that then call ``.format()`` are sinks for `CWE 134 <https://cwe.mitre.org/data/definitions/134.html>`_

* Exception objects have a new tainted attribute ``__traceback__``

* The ``next()`` method on iterable objects is now named ``__next__()``

* attributes on functions ``func_closure, func_code, func_defaults, func_dict, func_doc, func_globals, func_name`` were renamed to ``__closure__, __code__, __defaults__, __dict__, __doc__, __globals__, __name__``


* the ``__nonzero__()`` method is now ``__bool__()``

* The ``super()`` builtin function no longer requires an parameter; it propagates the current class by default

* Renamed builtin ``raw_input()`` to ``input()``. Py2's ``input()`` would eval and was risky. Py3's ``input()`` is safer -- it's now *just* a taint source
	
* ``intern()`` got moved into the ``sys`` module (it's now ``sys.intern()``)

* New keywords ``as`` and ``with``; I believe these are already supported (they were quietly introduced in 2.6, but are used more in Py3 code)
	* ``except Exception as var`` replaces ``except Exception, var`` syntax. Parser awareness

* New datatype ``OrderedDict`` -- for scan purposes, can be treated as a ``dict``

* ``str, bytes, bytearray`` all have ``maketrans(), translate()`` -- this used to be in the ``string`` module as ``struing.maketrans()``, but that's gone

* ``with`` statments can be compound as of 3.1: ``with open('mylog.txt') as infile, open('a.out', 'w') as outfile:`` makes ``infile, outfile`` available in that context's scope

* ``str.format_map()`` was added. Like ``str.format()`` but accepts mapping. Treat similarly.

* ``yeild from`` syntax added for `generator delegation <https://docs.python.org/3.3/whatsnew/3.3.html#pep-380>`_

* ``list`` and ``bytearray`` have a ``copy()`` method that propagates taint

* ``list`` and ``bytearray`` have a ``clear()`` method that should stop us following taint -- it empties the object of data

* Raw byte literals can be prefixed by ``rb`` *or* ``br``

* ``open()`` takes a named ``opener=`` parameter; it's a callable that recieves the arguments to open and returns a file descriptor. We may need to be aware of this for data/control flow

* Function definitions can be proceeded by ``async`` and ``await``; parser awareness

* A new operator is defined: ``@`` for matrix multiplication. No builtins support this, so it'll be up to libraries to implement class behavior. By default, we should assume in propagates structures

* ``os.scandir()`` is a new **source** for filenames

* ``subprocess.run()`` is a new **sink** for OS command injection


Packaging considerations
-------------------------------------------------------------------------------

*  A ``.zip`` that has a ``__main__.py`` inside can be executed directly by the intepreter
* ``import`` doesn't need ``__init__.py`` to make namespaces work anymore. ``import bar.foo`` will import a ``bar/foo.py`` relative to any package search path even if ``bar/__init__.py`` doesn't exist


dict and set comprehensions
------------------------------------------------------------------------------

Similar to list comprehensions, there are now comprehensions for the ``dict`` and ``set`` types:

.. code-block:: python

	new_dict = {k: v for k, v in old_dict}
	new_set = {x for x in some_set}


These can function as propagators much the same way list comprehensions do


Changes to stdlib
==============================================================================

These are the changes from py2.x to the stdlib culminating in python 3.5, which are relevant to scanning

    **SCOPE NOTE** -- these changes will be documented in the future. Work has begun to document these changes in `Python3.0-3.5_changes.rst`_


.. _Python3.0-3.5_changes.rst: Python3.0-3.5_changes.rst