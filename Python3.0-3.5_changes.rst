Changes from Python 2.x
------------------------------------------------------------------------------

3.0 introduced
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* ``print()`` expressed as function -- already supported because of Python2's ``from __future__ import print_function``
* ``dict.keys()`` reutrns a view of type ``dict_keys`` -- this can be treated like a list for our purposes, but is a different iterable datatype
* ``dict.items()`` reutrns a view of type ``dict_items`` -- this can be treated like a list for our purposes, but is a different iterable datatype
* ``dict.values()`` reutrns a view of type ``dict_keys`` -- this can be treated like a list for our purposes, but is a different iterable datatype
* ``dict.iterkeys()``, ``dict.iteritems()``, ``dict.itervalues()`` no longer exist
* ``map()`` returns an interator instead of a list -- this can be treated like a list for our purposes
* ``filter()`` returns an interator instead of a list -- this can be treated like a list for our purposes
* (TEST) ``range()`` now does what Py2's ``xrange()`` did, and the latter doesn't exist
* ``zip()`` returns an interator instead of a list -- this can be treated like a list for our purposes
* Ordering operations have subtly changed -- this shouldn't cause issues for our scans
* ``long`` datatype no longer exists. Only ``int``, which behaves mostly like ``long`` did. No scan effect unless we make a scan for range overflows
* integer division with `/` will return a float if the result requires it. Must use `//` to force integer division truncation -- no effect on scans
* String representations of integers have changed slightly -- no effect on scans
* (TEST) A bunch of things to make most string/text types *Unicode by default* -- may effect encoding scans if we have any
* (TEST) ``StringIO`` and ``cStringIO`` are replaced by ``io.StringIO`` and ``io.BytesIO``
* Annotations: these might change how we model future frameworks, but no scan effect for now
    * (TEST) You can annotate `Parameters <https://www.python.org/dev/peps/pep-3107/#parameters>`_
    * (TEST) You can annotate `Return Values <https://www.python.org/dev/peps/pep-3107/#return-values>`_
* functions can have `keyword only arguments <https://www.python.org/dev/peps/pep-3102/>`_ -- until our scanner can follow taint between functions, this isn't testable
* (TEST) ``nonlocal`` keyword to assign to a variable in a scope above the current scope
* (TEST) `extended iterable unpacking <http://www.python.org/dev/peps/pep-3132>`_ -- check to make sure this propagates correctly
* (TEST?) set and dict comprehensions -- ``{x for x in some_set}`` and ``{k: v for k, v in some_dict}``
* (TEST) new function ``bin()`` to convert integers to a binary repr
* (TEST) ``bytes()`` and ``b"string"`` notation for byte (non-unicode) strings
* You can now ``raise Exception from EarlierException`` -- no effect on current scans
* ``as`` and ``with``; technically introduced in 2.6, so shouldn't require effort to support in Py3
* ``except Exception as var`` replaces ``except Exception, var`` syntax
* Metaclass changes -- syntax is now ``class C(metaclass=M)``; since we don't support metaclasses, no work to be done
* List comprehensions work a little differently:
	* Slight syntax change: ``[x for x in item, item2]`` is now ``[x for x in (item, item2)]``
	* (TEST?) Loop control variables no longer accessible outside the scope of a comprehension
* Elipsis (``...``) can be used anywhere
* Some syntax removed -- not relevant
* ``exec()`` slightly changed -- no longer accepts a stream, no longer works as a keyword (funciton only). This makes things easier, I don't think there's any work to do
* Some `stdlib`_ modules were removed
* Some `stdlib`_ modules were *renamed*
	* ``_winreg`` is now ``winreg``
	* ``ConfigParser`` is now ``configparser``
	* ``copy_reg`` is now ``copyreg``
	* ``Queue`` is now ``queue``
	* ``SocketServer`` is now ``socketserver``
	* ``markupbase`` is now ``_markupbase``
	* ``repr`` is now ``reprlib``
	* ``test.test_support`` is now ``test.support``
	* ``__builtin__`` is now ``builtins`` (**NB:** the varaible ``__builtins__`` still exists and should not be confused)
* Some `stdlib`_ modules were *reogranized*
	* ``(anydbm, dbhash, dbm, dumbdbm, gdbm, whichdb)`` are now submodules of ``dbm``
	* ``(HTMLParser, htmlentitydefs)`` are now submodules of ``html``
	* ``(httplib, BaseHTTPServer, CGIHTTPServer, SimpleHTTPServer, Cookie, cookielib)`` are now submodules of ``http``
	* All the ``Tkinter`` related modules are now submodules of ``tkinter`` (except ``turtle`` because reasons)
	* ``(urllib, urllib2, urlparse, robotparse)`` are now submodules of ``urllib``
	* ``(xmlrpclib, DocXMLRPCServer, SimpleXMLRPCServer)`` are now submodules of ``xmlrpc``
* Some `stdlib`_ **functions/attributes** were removed or altered:
	* Removed: ``sys.exitfunc(), sys.exc_clear(), sys.exc_type, sys.exc_value, sys.exc_traceback``
	* Removed: ``read(), write()`` from ``array.array``
	* Removed: ``operator.sequenceIncludes(), operator.isCallable()``
	* Removed: ``thread.acquire_lock(), thread.release_lock()`` -- now use ``thread.acquire(), thread.release()``
	* Removed: ``random.jumpahead()``
	* Removed: ``os.tmpnam(), os.tempnam(), os.tmpfile()`` -- this functionality is in the ``tempfile`` module
	* Altered: ``tokenize.tokenize()`` is the new entry point (``tokenize.generate_tokens()`` is deprecated)
	* Altered: ``string.letters, string.lowercase, string.uppercase`` are gone in favor of non-locale-specific alternatives
* (TEST?) string formatting syntax changed. Now uses ``str.format()`` ; this may have been backported to 2.6 -- do we support it already?
* Exception handling has a few changes, most are syntatic and described above, but:
	* Exception objects now have a ``__traceback__`` attribute that may probagate taint in the same way as ``sys.exc_info()``
* Some operator changes:
	* Removed: ``__getslice__(), __setslice__(), __delslice__()`` (now use ``__getitem__(slice())`` and friends)
	* Altered: ``next()`` method is now ``__next__()``
	* Removed: ``__oct()__, __hex()__`` methods. The ``oct()`` and ``hex()`` functions are the only path now
	* Removed: ``__members__, __methods__``
	* Renamed: ``func_closure, func_code, func_defaults, func_dict, func_doc, func_globals, func_name`` were renamed to ``__closure__, __code__, __defaults__, __dict__, __doc__, __globals__, __name__``
	* Renamed: ``__nonzero__()`` is now ``__bool()__``
* New builtins:
	* Improved ``super()``: no longer requires arguments, otherwise behaves the same
	* (TEST) Renamed: ``raw_input()`` is now ``input()``, old ``input()`` behavior simualted with ``eval(input())``; this changes ``input()`` away from inherently risky and makes it just a taint source
	* Added: ``next()`` builtin function calls its argument's ``__next__()`` method
	* Moved: ``intern()`` is now in the ``sys`` module as ``sys.intern()``
	* Removed: ``apply()``. Instead of ``apply(f, args)`` use ``f(*args)``.
	* Removed ``callable()``. Instead of ``callable(f)`` you can use ``hasattr(f, '__call__')``. The ``operator.isCallable()`` function is also gone as noted above
	* Removed: ``coerce()``. This function no longer serves a purpose now that classic classes are gone.
	* Removed: ``execfile()``. Instead of ``execfile(fn)`` use ``exec(open(fn).read())``.
	* Removed: file. Use open().
	* Removed: reduce(). Use functools.reduce() if you really need it; however, 99 percent of the time an explicit for loop is more readable
	* Removed: reload(). Use imp.reload().
	* Removed: dict.has_key() – use the in operator instead.
* Some C API changes (out of scope)

3.1 introduced
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* (TEST) Ordered dictionaries. For scans, treat ``OrderedDict()`` constructor as a ``dict``; that's close enough for scans
* New "thousands separator" format string command for inlcuding thousands seps in formatted int/float values (``',d'``, e.g.)l no scan effect
* (Packaging) a .zip containing a ``__main__.py`` can now be executed by the python interpreter
* Added: ``int.bit_length()`` method added; how many bits it takes to represent a given ``int``; no scan effect
* Format strings can be auto-numbered; no scan effect
* (TEST?) Removed: ``string.maketrans()`` -- replaced by ``bytes.maketrans()`` and ``bytearray.maketrans()``; now all of ``str, bytes, bytarray`` have ``maketrans()`` and ``translate()`` methods.
* (TEST) ``with`` can be compound now: ``with open('mylog.txt') as infile, open('a.out', 'w') as outfile:``
* Modified: ``round()`` will now return an integer if its first argument is an integer; it used to always return a float
* (TEST) Added: ``collections.Counter(list)``; returned ``Counter`` object's keys will be unique values of the list (propagating) and values are integer frequency counts (e.g. if 'blue' is in the list three times ``Counter['blue'] == 3``)
* Added: ``tkinter.ttk`` ; out of scope, we don't support Tk details
* Can use ``with`` on ``gzip.GzipFile`` and ``bz2.BZ2File``
* Added: ``decimal.Decimal.from_float()`` constructor
* Added: ``itertools.combinations_with_replacement()`` generates permutations and Cartesian products
* (TEST?) Added **propagator**: ``itertools.compress(iterable, selector)``, equivalent to ``(d for d, s in zip(data,selector) if s)``
* ``re.sub(), re.subn(), re.split()`` support flags
* (TEST?) ``logging`` now has a ``NullHandler``, if set, log calls that use that handler will do effectively nothing
* ``pdb`` can now load anything that supports `PEP 302 <http://www.python.org/dev/peps/pep-0302>`_
* ``functools.partial`` objects can be sent to ``pickle``
* ``unittest`` lets you skip individual tests or classes but using annotations like ``@skipUnless``
* ``unittest`` lest you test expected failures with ``@expectedFailure``
* Added: ``assertSetEqual(), assertDictEqual(), assertDictContainsSubset(), assertListEqual(), assertTupleEqual(), assertSequenceEqual(), assertRaisesRegexp(), assertIsNone(), assertIsNotNone()`` to ``unittest``
* Added: constants ``SEEK_SET, SEEK_CUR, SEEK_END`` in ``io`` (for use by ``io.seek()``)
* ``sys.versioninfo`` is now a named tuple
* ``nntplib`` and ``imaplib`` now support IPv6
* ``pickle`` got more compatible
* Added: ``importlib`` - reference implementation of the import system in pure Python
* ``json`` now only works with ``str`` type, not any form of ``bytes``

3.2 introduced
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* (TEST?)(NEW module) the ``argparse`` module as an alternative to ``optparse``
* ``logging`` added ``logging.config.dictConfig()`` which allows specifying formatters and such as a ``dict``
* ``concurrent`` for managing concurrency -- out of scope because hard; 3.2 adds only ``concurrent.futures``
* Pycache system changes, which mean:
	* imported modules have a ``__cached__`` attribute with the cache file name (if any) from which they were loaded
	* the ``imp`` module now has a ``get_tag()`` method that contains the interpreter name tag (e.g. ``cpython-32``)
	* ``imp.source_from_cache(), imp.cache_from_source()`` should be used to map source file to cache file names
	* updates to ``py_compile`` and ``compileall`` to deal with these changes
	* ``importlib.abc`` has new Abstract Base Classes, deprecating ``PyLoader`` and ``PyPycLoader``
* WSGI improvements for header handling as ``str``:
	* (TEST?) New **source** ``wsgiref.handlers.read_environ()`` for transcoding CGI variables from ``os.environ`` into native strings.
* (TEST?) New **propagator** ``str.format_map()`` added; like ``str.format()`` but accepts mappings
* ``hasattr()`` more strict
* ``str()`` of a float or complex number now matches its ``repr()``
* ``memoryview.release()`` method
* ``memoryview`` objects can be used with ``with``
* can now delete a name from the namespace even if was previously used in a nested block
* C structures are now named tuples, e.g. ``os.stat(), time.gmtime(), sys.version_info`` all return classes that work like named tuples
* ``PTYHONWARNINGS`` env var as substitute for ``-W`` command line flag
* ``ResourceWarning`` added
* ``range.count()`` and ``range.index()``
* ``callable()`` is back -- returns a boolean
* non-ASCII support for imports
* Module changes:
	* Updates to ``email``:
		* ``message_from_bytes(), message_from_binary_file(), BytesFeedParser, BytesParser`` -- new **sources**
		* better encoding handling
		* ``BytesGenerator`` class -- ???
		* ``smtplib.SMTP`` class accepts these byte strings for ``sendmail()``
		* ``smtplib.SMTP.send_message`` accepts a ``email.Message`` object
	* Updates to ``xml.etree.ElementTree``:
		* Added: ``xml.etree.ElementTree.fromstringlist()`` which builds an XML document from a sequence of fragments
		* Added: ``xml.etree.ElementTree.register_namespace()`` for registering a global namespace prefix
		* Added: ``xml.etree.ElementTree.tostringlist()`` for string representation including all sublists
		* Added: ``xml.etree.ElementTree.Element.extend()`` for appending a sequence of zero or more elements
		* Added: ``xml.etree.ElementTree.Element.iterfind()`` searches an element and subelements
		* Added: ``xml.etree.ElementTree.Element.itertext()`` creates a text iterator over an element and its subelements
		* Added: ``xml.etree.ElementTree.TreeBuilder.end()`` closes the current element
		* Added: ``xml.etree.ElementTree.TreeBuilder.doctype()`` handles a doctype declaration
	* Updates to ``functools``
		* Added: ``@functools.lru_cache()`` decorator for caching results:
			* injects ``cache_info(), cache_clear()`` methods on the decorated function
		* Modified: ``@functools.wraps()`` now injects a ``__wrapped__`` attributed
		* Added: ``@functools.total_ordering()``; will auto-create comparison methods based on defining complements. E.g. if ``.__eq__`` and ``.__lt__`` are defined, it can inject ``__le__, __gt__, __ge__``
		* (???) Added: ``functools.cmp_to_key()`` 
	* Updates to ``itertools``:
		* Added: ``accumulate()``
	* Updates to ``collections``:
		* Added: ``collections.Counter.subtract()``
		* (TEST?) Added new **propagator**: ``collections.OrderedDict.move_to_end()``
		* Added: ``collections.deque.count()`` and ``collections.deque.reverse()``
	* Updates to ``threading``:
		* Added: ``Barrier`` class for making multiple threads wait
	* Updates to ``datetime`` and ``time``:
		* Added: ``datetime.timezone`` type
	* Updates to ``math``:
		* Added: ``isfinite(), expm1(), erf(), erfc(), gamma(), lgamma()``
	* Updates to ``abc``:
		* Added: ``@abc.abstractclassmethod`` decorator that requires a given class method to be implemented
		* Added: ``@abc.abstractstaticmethod`` deocrator that requires a given static method to be implemented
	* Updates to ``io``:
		* Added: ``io.BytesIO.getbuffer()`` -- provides an editable view of data without making a copy
	* Updates to ``reprlib``:
		* Added: ``@reprlib.recursive_repr``
	* Updates to ``csv``:
		* Added: dialect ``unix_dialect`` using ``dialect='unix'`` in constructors
		* Added new **sink**: ``csv.DictWriter.writeheader()`` to write a header row  (but maybe no risk we care about?)
	* Updates to ``contextlib``:
		* Added: |ContextDecorator|_, a class you can extend to make a decorator that also works as a context manager
		* Added: ``@contextmanager`` which implements ``ContextDecorator``
	* Updates to ``decimal``:
		* ``decimal.Decimal.from_float()`` is deprecated, constructor now can take a float
	* Updates to ``fractions``:
		* ``fractions.Fraction.from_decimal(), fractions.Fraction.from_float()`` are deprecated, constructor now takes a float
	* Updates to ``ftp``:
		* context managers used to auto-close connections as needed
	* Updates to ``gzip`` and ``zipfile``:
		* Modified: ``gzip.GzipFile`` inherits ``io.BufferedIOBase`` and adds a ``peek()`` method
		* Added new **propagator**: ``gzip.compress(), gzip.decompress()`` for in-memory compression/decompression
	* Updates to ``ast``:
		* (TEST?) Added: ``ast.literal_eval()`` -- claims to be a secure replacement for ``eval()``
	* Updates to ``os``:
		* Added new **cleanser**: ``fsencode()`` -- encodes filesystem paths for the current environ
		* Added new **propagator**: ``fsdecode()`` -- encodes/decodes filesystem paths for the current environ
		* Added new **source**: ``getenvb(), environb`` -- function, attribute that contains byte version of ENV vars
	* Updates to ``shutil``:
		* Added: archive support, mainly ``make_archive()`` (a new **sink**, no CWE) and ``unpack_archive()`` (a new **source**)	
	* Updates to ``sqlite3``:
		* Added new **risky** functions:  ``sqlite3.Connection.enable_load_extension()`` and ``sqlite3.Connection.load_extension()`` -- they load ``.so`` files; intent is to load SQLite extensions
	* New module ``html``:
		* Added new **cleanser**: ``escape()``
	* MORE TO DO

3.3 introduced
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* (???) ``yeild from`` for `generator delegation <https://docs.python.org/3.3/whatsnew/3.3.html#pep-380>`_
* Restored ``u'string'`` syntax for ``str`` objects
* Changed `IO Exception heirarchy <file:///Users/dmeyer/Documents/code-veracode/python3-api/sdoc/3.3/whatsnew/3.3.html#pep-3151>`_
* Security improvement: hash randomization is on by default
* Virtual environments added
* (PACKAGING) Added implicit namespace packages (see `PEP 420 <https://www.python.org/dev/peps/pep-0420/>`_); short version: you don't need to have an ``__init__.py`` in every circumstance; ``directory/foo.py`` can be loaded with ``import directory.foo`` as just a module
* Unicode code-point support is now complete, all unicode chars are acceptable inside a ``str``
	* indexes and ``len()`` and the like now properly work on *characters* not *bytes*; e.g. a multi-byte char not in the Basic Multilingual Plane (BMP) will have a ``len`` of ``1``
* Exception chain display can be supressed with ``raise Exception from None``
* Functions and class objects now have a ``__qualname__`` attribute that gives the full name of the object relative to the module where they're defined (see `PEP 3155 <file:///Users/dmeyer/Documents/code-veracode/python3-api/sdoc/3.3/whatsnew/3.3.html#pep-3155-qualified-name-for-classes-and-functions>`_)
* (TEST?) Added **propagator**: ``list.copy()`` and ``bytearray.copy()``
* Added ``list.clear(), bytearray.clear()`` that empty the data structures
* Raw byte literals can be ``rb"bytes"`` and not *just* ``br"bytes"``
* Modified: ``open()`` has an ``opener`` parameter that takes a callable to return the underlying file descriptor. This has an effect on control flow
* ``print()`` has a ``flush`` keyword to force stream flush
* ``str`` now has a ``casefold()`` method for case folding
* Module changes:
	* New modules:
		* Added: ``faulthandler`` (helps debugging low-level crashes)
		* Added: ``ipaddress`` (high-level objects representing IP addresses and masks)
		* Added: ``lzma`` (compress data using the XZ / LZMA algorithm)
		* Added: ``unittest.mock`` (replace parts of your system under test with mock objects)
		* Added: ``venv`` (Python virtual environments, as in the popular virtualenv package)
	* Changes to ``inspect``:
		* Added: ``inspect.signature()`` to inespect callables; added objects ``inspect.Signature, inspect.Parameter, inspect.BoundArguments`` to support this
	* MORE TO DO

3.4 introduced
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**NB:** more than half of Py3 webapps surveyed use this version, per `w3techs retrieved 07 June 2018 <https://w3techs.com/technologies/details/pl-python/3/all>`_

* Security imrovements:
	* Secure and interchangeable hash algorithm (PEP 456).
	* Make newly created file descriptors non-inheritable (PEP 446) to avoid leaking file descriptors to child processes.
	* New command line option for isolated mode, (issue 16499).
	* ``multiprocessing ``now has an option to avoid using os.fork on Unix. spawn and forkserver are more secure because they avoid sharing data with child processes.
	* multiprocessing child processes on Windows no longer inherit all of the parent’s inheritable handles, only the necessary ones.
	* (???) A new ``hashlib.pbkdf2_hmac()`` function provides the PKCS#5 password-based key derivation function 2 -- may be relevant if we flag proper KDF usage for password storage/etc.
	* TLSv1.1 and TLSv1.2 support for ``ssl``.
	* Retrieving certificates from the Windows system cert store support for ``ssl``.
	* Server-side SNI (Server Name Indication) support for ``ssl``.
	* The ``ssl.SSLContext`` class has a lot of improvements.
	* All modules in the standard library that support SSL now support server certificate verification, including hostname matching (``ssl.match_hostname()``) and CRLs (Certificate Revocation lists, see ``ssl.SSLContext.load_verify_locations()``).
* (???) File descriptors are marked non-inheritable on creation; could affect data flow model
* (???) Module ``__file__`` attributes (and related values) should now always contain absolute paths by default, with the sole exception of ``__main__.__file__`` when a script has been executed directly using a relative path. (Contributed by Brett Cannon in issue 18416.) -- alters the use of this attribute as a taint source for path injection flaws (makes it safer)
* Module changes:
	* New modules:
		* Added: ``asyncio``: New provisional API for asynchronous IO (PEP 3156).
		* Added: ``ensurepip``: Bootstrapping the pip installer (PEP 453).
		* Added: ``enum``: Support for enumeration types (PEP 435).
		* Added: ``pathlib``: Object-oriented filesystem paths (PEP 428).
		* Added: ``selectors``: High-level and efficient I/O multiplexing, built upon the select module primitives (part of PEP 3156).
		* Added: ``statistics``: A basic numerically stable statistics library (PEP 450).
		* Added: ``tracemalloc``: Trace Python memory allocations (PEP 454).
	* MORE TO DO

3.5 introduced
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* (TEST?) Coroutines with ``async`` and ``await`` syntax (`PEP 492 <file:///Users/dmeyer/Documents/code-veracode/python3-api/sdoc/3.5/whatsnew/3.5.html#whatsnew-pep-492>`_); key for modeling if we care about asynchronous models for any flaws, otherwise probably out of scope except to make sure it doesn't ruin our ability to see definitions
* Added new **operator**: ``@`` for matrix-multiplication (`PEP 465 <file:///Users/dmeyer/Documents/code-veracode/python3-api/sdoc/3.5/whatsnew/3.5.html#whatsnew-pep-465>`_); no builtins support it yet, but classes can define `` __matmul__(), __rmatmul__(), __imatmul__()`` to implement it -- may affect data flow modeling
* (???) Modified: the ``*`` and ``**`` unpacking operators can do more stuff (`PEP 448 <file:///Users/dmeyer/Documents/code-veracode/python3-api/sdoc/3.5/whatsnew/3.5.html#whatsnew-pep-448>`_) -- not sure if this has an impact on scans
* Added: ``bytes, bytearray, memoryview`` all have a ``hex()`` method to represent bytes as a string of hexadecimal codes
* Added: generators now have attribute ``gi_yieldfrom`` which returns the object being iterated by ``yield`` -- maybe a new propagator?
* Added new **sink**: ``os.scandir()`` for directory traversal, new sink for dir traversal issues (maybe?)
* Added new **sink**: ``subprocess.run()``, new sink for OS command injection if only one positional argument and it's tainted
* SSLv3 now disabled in stdlib by default
* Module changes:
	* MORE TO DO

3.6 introduced
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




.. |ContextDecorator| replace:: ``ContextDecorator``
.. _ContextDecorator: https://docs.python.org/3.2/library/contextlib.html#contextlib.ContextDecorator

