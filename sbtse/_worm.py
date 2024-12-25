r"""Wrapper for WormDLL.h

Generated with:
ctypesgen -llibWormAPI WormDLL.h WormDLL_publicTypes.h wormError.h -o _worm.py

Do not modify this file.
"""

__docformat__ = "restructuredtext"

# Begin preamble for Python

import ctypes
import sys
from ctypes import *  # noqa: F401, F403

_int_types = (ctypes.c_int16, ctypes.c_int32)
if hasattr(ctypes, "c_int64"):
    # Some builds of ctypes apparently do not have ctypes.c_int64
    # defined; it's a pretty good bet that these builds do not
    # have 64-bit pointers.
    _int_types += (ctypes.c_int64,)
for t in _int_types:
    if ctypes.sizeof(t) == ctypes.sizeof(ctypes.c_size_t):
        c_ptrdiff_t = t
del t
del _int_types


class UserString:
    def __init__(self, seq):
        if isinstance(seq, bytes):
            self.data = seq
        elif isinstance(seq, UserString):
            self.data = seq.data[:]
        else:
            self.data = str(seq).encode()

    def __bytes__(self):
        return self.data

    def __str__(self):
        return self.data.decode()

    def __repr__(self):
        return repr(self.data)

    def __int__(self):
        return int(self.data.decode())

    def __long__(self):
        return int(self.data.decode())

    def __float__(self):
        return float(self.data.decode())

    def __complex__(self):
        return complex(self.data.decode())

    def __hash__(self):
        return hash(self.data)

    def __le__(self, string):
        if isinstance(string, UserString):
            return self.data <= string.data
        else:
            return self.data <= string

    def __lt__(self, string):
        if isinstance(string, UserString):
            return self.data < string.data
        else:
            return self.data < string

    def __ge__(self, string):
        if isinstance(string, UserString):
            return self.data >= string.data
        else:
            return self.data >= string

    def __gt__(self, string):
        if isinstance(string, UserString):
            return self.data > string.data
        else:
            return self.data > string

    def __eq__(self, string):
        if isinstance(string, UserString):
            return self.data == string.data
        else:
            return self.data == string

    def __ne__(self, string):
        if isinstance(string, UserString):
            return self.data != string.data
        else:
            return self.data != string

    def __contains__(self, char):
        return char in self.data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.__class__(self.data[index])

    def __getslice__(self, start, end):
        start = max(start, 0)
        end = max(end, 0)
        return self.__class__(self.data[start:end])

    def __add__(self, other):
        if isinstance(other, UserString):
            return self.__class__(self.data + other.data)
        elif isinstance(other, bytes):
            return self.__class__(self.data + other)
        else:
            return self.__class__(self.data + str(other).encode())

    def __radd__(self, other):
        if isinstance(other, bytes):
            return self.__class__(other + self.data)
        else:
            return self.__class__(str(other).encode() + self.data)

    def __mul__(self, n):
        return self.__class__(self.data * n)

    __rmul__ = __mul__

    def __mod__(self, args):
        return self.__class__(self.data % args)

    # the following methods are defined in alphabetical order:
    def capitalize(self):
        return self.__class__(self.data.capitalize())

    def center(self, width, *args):
        return self.__class__(self.data.center(width, *args))

    def count(self, sub, start=0, end=sys.maxsize):
        return self.data.count(sub, start, end)

    def decode(self, encoding=None, errors=None):  # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.decode(encoding, errors))
            else:
                return self.__class__(self.data.decode(encoding))
        else:
            return self.__class__(self.data.decode())

    def encode(self, encoding=None, errors=None):  # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.encode(encoding, errors))
            else:
                return self.__class__(self.data.encode(encoding))
        else:
            return self.__class__(self.data.encode())

    def endswith(self, suffix, start=0, end=sys.maxsize):
        return self.data.endswith(suffix, start, end)

    def expandtabs(self, tabsize=8):
        return self.__class__(self.data.expandtabs(tabsize))

    def find(self, sub, start=0, end=sys.maxsize):
        return self.data.find(sub, start, end)

    def index(self, sub, start=0, end=sys.maxsize):
        return self.data.index(sub, start, end)

    def isalpha(self):
        return self.data.isalpha()

    def isalnum(self):
        return self.data.isalnum()

    def isdecimal(self):
        return self.data.isdecimal()

    def isdigit(self):
        return self.data.isdigit()

    def islower(self):
        return self.data.islower()

    def isnumeric(self):
        return self.data.isnumeric()

    def isspace(self):
        return self.data.isspace()

    def istitle(self):
        return self.data.istitle()

    def isupper(self):
        return self.data.isupper()

    def join(self, seq):
        return self.data.join(seq)

    def ljust(self, width, *args):
        return self.__class__(self.data.ljust(width, *args))

    def lower(self):
        return self.__class__(self.data.lower())

    def lstrip(self, chars=None):
        return self.__class__(self.data.lstrip(chars))

    def partition(self, sep):
        return self.data.partition(sep)

    def replace(self, old, new, maxsplit=-1):
        return self.__class__(self.data.replace(old, new, maxsplit))

    def rfind(self, sub, start=0, end=sys.maxsize):
        return self.data.rfind(sub, start, end)

    def rindex(self, sub, start=0, end=sys.maxsize):
        return self.data.rindex(sub, start, end)

    def rjust(self, width, *args):
        return self.__class__(self.data.rjust(width, *args))

    def rpartition(self, sep):
        return self.data.rpartition(sep)

    def rstrip(self, chars=None):
        return self.__class__(self.data.rstrip(chars))

    def split(self, sep=None, maxsplit=-1):
        return self.data.split(sep, maxsplit)

    def rsplit(self, sep=None, maxsplit=-1):
        return self.data.rsplit(sep, maxsplit)

    def splitlines(self, keepends=0):
        return self.data.splitlines(keepends)

    def startswith(self, prefix, start=0, end=sys.maxsize):
        return self.data.startswith(prefix, start, end)

    def strip(self, chars=None):
        return self.__class__(self.data.strip(chars))

    def swapcase(self):
        return self.__class__(self.data.swapcase())

    def title(self):
        return self.__class__(self.data.title())

    def translate(self, *args):
        return self.__class__(self.data.translate(*args))

    def upper(self):
        return self.__class__(self.data.upper())

    def zfill(self, width):
        return self.__class__(self.data.zfill(width))


class MutableString(UserString):
    """mutable string objects

    Python strings are immutable objects.  This has the advantage, that
    strings may be used as dictionary keys.  If this property isn't needed
    and you insist on changing string values in place instead, you may cheat
    and use MutableString.

    But the purpose of this class is an educational one: to prevent
    people from inventing their own mutable string class derived
    from UserString and than forget thereby to remove (override) the
    __hash__ method inherited from UserString.  This would lead to
    errors that would be very hard to track down.

    A faster and better solution is to rewrite your program using lists."""

    def __init__(self, string=""):
        self.data = string

    def __hash__(self):
        raise TypeError("unhashable type (it is mutable)")

    def __setitem__(self, index, sub):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data):
            raise IndexError
        self.data = self.data[:index] + sub + self.data[index + 1 :]

    def __delitem__(self, index):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data):
            raise IndexError
        self.data = self.data[:index] + self.data[index + 1 :]

    def __setslice__(self, start, end, sub):
        start = max(start, 0)
        end = max(end, 0)
        if isinstance(sub, UserString):
            self.data = self.data[:start] + sub.data + self.data[end:]
        elif isinstance(sub, bytes):
            self.data = self.data[:start] + sub + self.data[end:]
        else:
            self.data = self.data[:start] + str(sub).encode() + self.data[end:]

    def __delslice__(self, start, end):
        start = max(start, 0)
        end = max(end, 0)
        self.data = self.data[:start] + self.data[end:]

    def immutable(self):
        return UserString(self.data)

    def __iadd__(self, other):
        if isinstance(other, UserString):
            self.data += other.data
        elif isinstance(other, bytes):
            self.data += other
        else:
            self.data += str(other).encode()
        return self

    def __imul__(self, n):
        self.data *= n
        return self


class String(MutableString, ctypes.Union):

    _fields_ = [("raw", ctypes.POINTER(ctypes.c_char)), ("data", ctypes.c_char_p)]

    def __init__(self, obj=b""):
        if isinstance(obj, (bytes, UserString)):
            self.data = bytes(obj)
        else:
            self.raw = obj

    def __len__(self):
        return self.data and len(self.data) or 0

    def from_param(cls, obj):
        # Convert None or 0
        if obj is None or obj == 0:
            return cls(ctypes.POINTER(ctypes.c_char)())

        # Convert from String
        elif isinstance(obj, String):
            return obj

        # Convert from bytes
        elif isinstance(obj, bytes):
            return cls(obj)

        # Convert from str
        elif isinstance(obj, str):
            return cls(obj.encode())

        # Convert from c_char_p
        elif isinstance(obj, ctypes.c_char_p):
            return obj

        # Convert from POINTER(ctypes.c_char)
        elif isinstance(obj, ctypes.POINTER(ctypes.c_char)):
            return obj

        # Convert from raw pointer
        elif isinstance(obj, int):
            return cls(ctypes.cast(obj, ctypes.POINTER(ctypes.c_char)))

        # Convert from ctypes.c_char array
        elif isinstance(obj, ctypes.c_char * len(obj)):
            return obj

        # Convert from object
        else:
            return String.from_param(obj._as_parameter_)

    from_param = classmethod(from_param)


def ReturnString(obj, func=None, arguments=None):
    return String.from_param(obj)


# As of ctypes 1.0, ctypes does not support custom error-checking
# functions on callbacks, nor does it support custom datatypes on
# callbacks, so we must ensure that all callbacks return
# primitive datatypes.
#
# Non-primitive return values wrapped with UNCHECKED won't be
# typechecked, and will be converted to ctypes.c_void_p.
def UNCHECKED(type):
    if hasattr(type, "_type_") and isinstance(type._type_, str) and type._type_ != "P":
        return type
    else:
        return ctypes.c_void_p


# ctypes doesn't have direct support for variadic functions, so we have to write
# our own wrapper class
class _variadic_function(object):
    def __init__(self, func, restype, argtypes, errcheck):
        self.func = func
        self.func.restype = restype
        self.argtypes = argtypes
        if errcheck:
            self.func.errcheck = errcheck

    def _as_parameter_(self):
        # So we can pass this variadic function as a function pointer
        return self.func

    def __call__(self, *args):
        fixed_args = []
        i = 0
        for argtype in self.argtypes:
            # Typecheck what we can
            fixed_args.append(argtype.from_param(args[i]))
            i += 1
        return self.func(*fixed_args + list(args[i:]))


def ord_if_char(value):
    """
    Simple helper used for casts to simple builtin types:  if the argument is a
    string type, it will be converted to it's ordinal value.

    This function will raise an exception if the argument is string with more
    than one characters.
    """
    return ord(value) if (isinstance(value, bytes) or isinstance(value, str)) else value


# End preamble

_libs = {}
_libdirs = []

# Begin loader

"""
Load libraries - appropriately for all our supported platforms
"""
# ----------------------------------------------------------------------------
# Copyright (c) 2008 David James
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

import ctypes
import ctypes.util
import glob
import os.path
import platform
import re
import sys


def _environ_path(name):
    """Split an environment variable into a path-like list elements"""
    if name in os.environ:
        return os.environ[name].split(":")
    return []


class LibraryLoader:
    """
    A base class For loading of libraries ;-)
    Subclasses load libraries for specific platforms.
    """

    # library names formatted specifically for platforms
    name_formats = ["%s"]

    class Lookup:
        """Looking up calling conventions for a platform"""

        mode = ctypes.DEFAULT_MODE

        def __init__(self, path):
            super(LibraryLoader.Lookup, self).__init__()
            self.access = dict(cdecl=ctypes.CDLL(path, self.mode))

        def get(self, name, calling_convention="cdecl"):
            """Return the given name according to the selected calling convention"""
            if calling_convention not in self.access:
                raise LookupError(
                    "Unknown calling convention '{}' for function '{}'".format(
                        calling_convention, name
                    )
                )
            return getattr(self.access[calling_convention], name)

        def has(self, name, calling_convention="cdecl"):
            """Return True if this given calling convention finds the given 'name'"""
            if calling_convention not in self.access:
                return False
            return hasattr(self.access[calling_convention], name)

        def __getattr__(self, name):
            return getattr(self.access["cdecl"], name)

    def __init__(self):
        self.other_dirs = []

    def __call__(self, libname):
        """Given the name of a library, load it."""
        paths = self.getpaths(libname)

        for path in paths:
            # noinspection PyBroadException
            try:
                return self.Lookup(path)
            except Exception:  # pylint: disable=broad-except
                pass

        raise ImportError("Could not load %s." % libname)

    def getpaths(self, libname):
        """Return a list of paths where the library might be found."""
        if os.path.isabs(libname):
            yield libname
        else:
            # search through a prioritized series of locations for the library

            # we first search any specific directories identified by user
            for dir_i in self.other_dirs:
                for fmt in self.name_formats:
                    # dir_i should be absolute already
                    yield os.path.join(dir_i, fmt % libname)

            # check if this code is even stored in a physical file
            try:
                this_file = __file__
            except NameError:
                this_file = None

            # then we search the directory where the generated python interface is stored
            if this_file is not None:
                for fmt in self.name_formats:
                    yield os.path.abspath(
                        os.path.join(os.path.dirname(__file__), fmt % libname)
                    )

            # now, use the ctypes tools to try to find the library
            for fmt in self.name_formats:
                path = ctypes.util.find_library(fmt % libname)
                if path:
                    yield path

            # then we search all paths identified as platform-specific lib paths
            for path in self.getplatformpaths(libname):
                yield path

            # Finally, we'll try the users current working directory
            for fmt in self.name_formats:
                yield os.path.abspath(os.path.join(os.path.curdir, fmt % libname))

    def getplatformpaths(self, _libname):  # pylint: disable=no-self-use
        """Return all the library paths available in this platform"""
        return []


# Darwin (Mac OS X)


class DarwinLibraryLoader(LibraryLoader):
    """Library loader for MacOS"""

    name_formats = [
        "lib%s.dylib",
        "lib%s.so",
        "lib%s.bundle",
        "%s.dylib",
        "%s.so",
        "%s.bundle",
        "%s",
    ]

    class Lookup(LibraryLoader.Lookup):
        """
        Looking up library files for this platform (Darwin aka MacOS)
        """

        # Darwin requires dlopen to be called with mode RTLD_GLOBAL instead
        # of the default RTLD_LOCAL.  Without this, you end up with
        # libraries not being loadable, resulting in "Symbol not found"
        # errors
        mode = ctypes.RTLD_GLOBAL

    def getplatformpaths(self, libname):
        if os.path.pathsep in libname:
            names = [libname]
        else:
            names = [fmt % libname for fmt in self.name_formats]

        for directory in self.getdirs(libname):
            for name in names:
                yield os.path.join(directory, name)

    @staticmethod
    def getdirs(libname):
        """Implements the dylib search as specified in Apple documentation:

        http://developer.apple.com/documentation/DeveloperTools/Conceptual/
            DynamicLibraries/Articles/DynamicLibraryUsageGuidelines.html

        Before commencing the standard search, the method first checks
        the bundle's ``Frameworks`` directory if the application is running
        within a bundle (OS X .app).
        """

        dyld_fallback_library_path = _environ_path("DYLD_FALLBACK_LIBRARY_PATH")
        if not dyld_fallback_library_path:
            dyld_fallback_library_path = [
                os.path.expanduser("~/lib"),
                "/usr/local/lib",
                "/usr/lib",
            ]

        dirs = []

        if "/" in libname:
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))
        else:
            dirs.extend(_environ_path("LD_LIBRARY_PATH"))
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))
            dirs.extend(_environ_path("LD_RUN_PATH"))

        if hasattr(sys, "frozen") and getattr(sys, "frozen") == "macosx_app":
            dirs.append(os.path.join(os.environ["RESOURCEPATH"], "..", "Frameworks"))

        dirs.extend(dyld_fallback_library_path)

        return dirs


# Posix


class PosixLibraryLoader(LibraryLoader):
    """Library loader for POSIX-like systems (including Linux)"""

    _ld_so_cache = None

    _include = re.compile(r"^\s*include\s+(?P<pattern>.*)")

    name_formats = ["lib%s.so", "%s.so", "%s"]

    class _Directories(dict):
        """Deal with directories"""

        def __init__(self):
            dict.__init__(self)
            self.order = 0

        def add(self, directory):
            """Add a directory to our current set of directories"""
            if len(directory) > 1:
                directory = directory.rstrip(os.path.sep)
            # only adds and updates order if exists and not already in set
            if not os.path.exists(directory):
                return
            order = self.setdefault(directory, self.order)
            if order == self.order:
                self.order += 1

        def extend(self, directories):
            """Add a list of directories to our set"""
            for a_dir in directories:
                self.add(a_dir)

        def ordered(self):
            """Sort the list of directories"""
            return (i[0] for i in sorted(self.items(), key=lambda d: d[1]))

    def _get_ld_so_conf_dirs(self, conf, dirs):
        """
        Recursive function to help parse all ld.so.conf files, including proper
        handling of the `include` directive.
        """

        try:
            with open(conf) as fileobj:
                for dirname in fileobj:
                    dirname = dirname.strip()
                    if not dirname:
                        continue

                    match = self._include.match(dirname)
                    if not match:
                        dirs.add(dirname)
                    else:
                        for dir2 in glob.glob(match.group("pattern")):
                            self._get_ld_so_conf_dirs(dir2, dirs)
        except IOError:
            pass

    def _create_ld_so_cache(self):
        # Recreate search path followed by ld.so.  This is going to be
        # slow to build, and incorrect (ld.so uses ld.so.cache, which may
        # not be up-to-date).  Used only as fallback for distros without
        # /sbin/ldconfig.
        #
        # We assume the DT_RPATH and DT_RUNPATH binary sections are omitted.

        directories = self._Directories()
        for name in (
            "LD_LIBRARY_PATH",
            "SHLIB_PATH",  # HP-UX
            "LIBPATH",  # OS/2, AIX
            "LIBRARY_PATH",  # BE/OS
        ):
            if name in os.environ:
                directories.extend(os.environ[name].split(os.pathsep))

        self._get_ld_so_conf_dirs("/etc/ld.so.conf", directories)

        bitage = platform.architecture()[0]

        unix_lib_dirs_list = []
        if bitage.startswith("64"):
            # prefer 64 bit if that is our arch
            unix_lib_dirs_list += ["/lib64", "/usr/lib64"]

        # must include standard libs, since those paths are also used by 64 bit
        # installs
        unix_lib_dirs_list += ["/lib", "/usr/lib"]
        if sys.platform.startswith("linux"):
            # Try and support multiarch work in Ubuntu
            # https://wiki.ubuntu.com/MultiarchSpec
            if bitage.startswith("32"):
                # Assume Intel/AMD x86 compat
                unix_lib_dirs_list += ["/lib/i386-linux-gnu", "/usr/lib/i386-linux-gnu"]
            elif bitage.startswith("64"):
                # Assume Intel/AMD x86 compatible
                unix_lib_dirs_list += [
                    "/lib/x86_64-linux-gnu",
                    "/usr/lib/x86_64-linux-gnu",
                ]
            else:
                # guess...
                unix_lib_dirs_list += glob.glob("/lib/*linux-gnu")
        directories.extend(unix_lib_dirs_list)

        cache = {}
        lib_re = re.compile(r"lib(.*)\.s[ol]")
        # ext_re = re.compile(r"\.s[ol]$")
        for our_dir in directories.ordered():
            try:
                for path in glob.glob("%s/*.s[ol]*" % our_dir):
                    file = os.path.basename(path)

                    # Index by filename
                    cache_i = cache.setdefault(file, set())
                    cache_i.add(path)

                    # Index by library name
                    match = lib_re.match(file)
                    if match:
                        library = match.group(1)
                        cache_i = cache.setdefault(library, set())
                        cache_i.add(path)
            except OSError:
                pass

        self._ld_so_cache = cache

    def getplatformpaths(self, libname):
        if self._ld_so_cache is None:
            self._create_ld_so_cache()

        result = self._ld_so_cache.get(libname, set())
        for i in result:
            # we iterate through all found paths for library, since we may have
            # actually found multiple architectures or other library types that
            # may not load
            yield i


# Windows


class WindowsLibraryLoader(LibraryLoader):
    """Library loader for Microsoft Windows"""

    name_formats = ["%s.dll", "lib%s.dll", "%slib.dll", "%s"]

    class Lookup(LibraryLoader.Lookup):
        """Lookup class for Windows libraries..."""

        def __init__(self, path):
            super(WindowsLibraryLoader.Lookup, self).__init__(path)
            self.access["stdcall"] = ctypes.windll.LoadLibrary(path)


# Platform switching

# If your value of sys.platform does not appear in this dict, please contact
# the Ctypesgen maintainers.

loaderclass = {
    "darwin": DarwinLibraryLoader,
    "cygwin": WindowsLibraryLoader,
    "win32": WindowsLibraryLoader,
    "msys": WindowsLibraryLoader,
}

load_library = loaderclass.get(sys.platform, PosixLibraryLoader)()


def add_library_search_dirs(other_dirs):
    """
    Add libraries to search paths.
    If library paths are relative, convert them to absolute with respect to this
    file's directory
    """
    for path in other_dirs:
        if not os.path.isabs(path):
            path = os.path.abspath(path)
        load_library.other_dirs.append(path)


del loaderclass

# End loader

add_library_search_dirs([])

# Begin libraries
_libs["libWormAPI"] = load_library("libWormAPI")

# 1 libraries
# End libraries

# No modules

enum_anon_1 = c_int  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL_publicTypes.h: 37

WORM_ENTRY_TYPE_TRANSACTION = 0  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL_publicTypes.h: 37

WORM_ENTRY_TYPE_SYSTEM_LOG_MESSAGE = 1  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL_publicTypes.h: 37

WORM_ENTRY_TYPE_SE_AUDIT_LOG_MESSAGE = 2  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL_publicTypes.h: 37

WormEntryType = enum_anon_1  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL_publicTypes.h: 37

enum_anon_2 = c_int  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL_publicTypes.h: 64

WORM_USER_UNAUTHENTICATED = 0  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL_publicTypes.h: 64

WORM_USER_ADMIN = 1  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL_publicTypes.h: 64

WORM_USER_TIME_ADMIN = 2  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL_publicTypes.h: 64

WormUserId = enum_anon_2  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL_publicTypes.h: 64

enum_anon_3 = c_int  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL_publicTypes.h: 95

WORM_INIT_UNINITIALIZED = 0  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL_publicTypes.h: 95

WORM_INIT_INITIALIZED = 1  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL_publicTypes.h: 95

WORM_INIT_DECOMMISSIONED = 2  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL_publicTypes.h: 95

WormInitializationState = enum_anon_3  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL_publicTypes.h: 95

enum_anon_4 = c_int  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL_publicTypes.h: 109

WORM_FW_1_1_0_USB = 0  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL_publicTypes.h: 109

WORM_FW_NONE = (
    WORM_FW_1_1_0_USB + 1
)  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL_publicTypes.h: 109

WormTseFirmwareUpdate = enum_anon_4  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL_publicTypes.h: 109

enum_anon_5 = c_int  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_NOERROR = 0  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_INVALID_PARAMETER = 1  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_NO_WORM_CARD = 2  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_IO = 3  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_TIMEOUT = 4  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_OUTOFMEM = 5  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_INVALID_RESPONSE = 6  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_STORE_FULL_INTERNAL = 7  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_RESPONSE_MISSING = 8  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_EXPORT_NOT_INITIALIZED = 9  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_EXPORT_FAILED = 10  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_INCREMENTAL_EXPORT_INVALID_STATE = 11  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_INCREMENTAL_EXPORT_NO_DATA = 12  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_POWER_CYCLE_DETECTED = 13  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_FIRMWARE_UPDATE_NOT_APPLIED = 14  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_THREAD_START_FAILED = 15  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_NETWORK = 16  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_CMD_NOT_SUPPORTED = 17  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_LAN_INVALID_API_TOKEN = 18  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_NETWORK_TIMEOUT = 19  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_CONNECTION_FAILED = 20  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_LAN_UNBALANCED_LOCKS = 21  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_LAN_INVALID_SERVER_RESPONSE = 22  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_INVALID_STATE = 23  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_TSE_NOT_FOUND = 24  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_INCREMENTAL_EXPORT_LIMIT_TOO_LOW = 25  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_FWU_NOT_AVAILABLE = 26  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_FROM_CARD_FIRST = 0x1000  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_UNKNOWN = 0x1001  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_NO_TIME_SET = 0x1002  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_NO_TRANSACTION_IN_PROGRESS = 0x1004  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_INVALID_CMD_SYNTAX = 0x1005  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_WRONG_LENGTH = WORM_ERROR_INVALID_CMD_SYNTAX  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_NOT_ENOUGH_DATA_WRITTEN = 0x1006  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_TSE_INVALID_PARAMETER = 0x1007  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_TRANSACTION_NOT_STARTED = 0x1008  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_MAX_PARALLEL_TRANSACTIONS = 0x1009  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_CERTIFICATE_EXPIRED = 0x100A  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_NO_LAST_TRANSACTION = 0x100C  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_CMD_NOT_ALLOWED = 0x100D  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_TRANSACTION_SIGNATURES_EXCEEDED = 0x100E  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_NOT_AUTHORIZED = 0x100F  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_MAX_REGISTERED_CLIENTS_REACHED = 0x1010  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_CLIENT_NOT_REGISTERED = 0x1011  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_EXPORT_UNACKNOWLEDGED_DATA = 0x1012  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_CLIENT_HAS_UNFINISHED_TRANSACTIONS = 0x1013  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_TSE_HAS_UNFINISHED_TRANSACTIONS = 0x1014  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_TSE_NO_RESPONSE_TO_FETCH = 0x1015  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_NOT_ALLOWED_EXPORT_IN_PROGRESS = 0x1016  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_STORE_FULL = 0x1017  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_WRONG_STATE_NEEDS_PUK_CHANGE = 0x1050  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_WRONG_STATE_NEEDS_PIN_CHANGE = 0x1051  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_WRONG_STATE_NEEDS_ACTIVE_CTSS = 0x1053  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_WRONG_STATE_NEEDS_ACTIVE_ERS = WORM_ERROR_WRONG_STATE_NEEDS_ACTIVE_CTSS  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_WRONG_STATE_NEEDS_SELF_TEST = 0x1054  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_WRONG_STATE_NEEDS_SELF_TEST_PASSED = 0x1055  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_FWU_INTEGRITY_FAILURE = 0x1061  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_FWU_DECRYPTION_FAILURE = 0x1062  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_FWU_WRONG_FORMAT = 0x1064  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_FWU_INTERNAL_ERROR = 0x1065  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_FWU_DOWNGRADE_PROHIBITED = 0x1067  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_TSE_ALREADY_INITIALIZED = 0x10FD  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_TSE_DECOMMISSIONED = 0x10FE  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_TSE_NOT_INITIALIZED = 0x10FF  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_AUTHENTICATION_FAILED = 0x1100  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_AUTHENTICATION_PIN_BLOCKED = 0x1201  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_AUTHENTICATION_USER_NOT_LOGGED_IN = 0x1202  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_SELF_TEST_FAILED_FW = 0x1300  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_SELF_TEST_FAILED_CSP = 0x1310  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_SELF_TEST_FAILED_RNG = 0x1320  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_FWU_BASE_FW_ERROR = 0x1400  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_FWU_FWEXT_ERROR = 0x1500  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_FWU_CSP_ERROR = 0x1600  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_EXPORT_NONE_IN_PROGRESS = 0x2001  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_EXPORT_RETRY = 0x2002  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_EXPORT_NO_DATA_AVAILABLE = 0x2003  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_CMD_NOT_FOUND = 0xF000  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_SIG_ERROR = 0xFF00  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WORM_ERROR_FROM_CARD_LAST = 0xFFFF  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

WormError = enum_anon_5  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/wormError.h: 278

__uint8_t = c_ubyte  # /usr/include/bits/types.h: 38

__uint32_t = c_uint  # /usr/include/bits/types.h: 42

__uint64_t = c_ulong  # /usr/include/bits/types.h: 45

uint8_t = __uint8_t  # /usr/include/bits/stdint-uintn.h: 24

uint32_t = __uint32_t  # /usr/include/bits/stdint-uintn.h: 26

uint64_t = __uint64_t  # /usr/include/bits/stdint-uintn.h: 27

worm_uint = uint64_t  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 287


# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 309
class struct_WormContext(Structure):
    pass


WormContext = struct_WormContext  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 309

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 317
if _libs["libWormAPI"].has("worm_getVersion", "cdecl"):
    worm_getVersion = _libs["libWormAPI"].get("worm_getVersion", "cdecl")
    worm_getVersion.argtypes = []
    worm_getVersion.restype = c_char_p

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 328
if _libs["libWormAPI"].has("worm_isOnlineSdk", "cdecl"):
    worm_isOnlineSdk = _libs["libWormAPI"].get("worm_isOnlineSdk", "cdecl")
    worm_isOnlineSdk.argtypes = []
    worm_isOnlineSdk.restype = c_int

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 336
if _libs["libWormAPI"].has("worm_signatureAlgorithm", "cdecl"):
    worm_signatureAlgorithm = _libs["libWormAPI"].get(
        "worm_signatureAlgorithm", "cdecl"
    )
    worm_signatureAlgorithm.argtypes = []
    worm_signatureAlgorithm.restype = c_char_p

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 344
if _libs["libWormAPI"].has("worm_logTimeFormat", "cdecl"):
    worm_logTimeFormat = _libs["libWormAPI"].get("worm_logTimeFormat", "cdecl")
    worm_logTimeFormat.argtypes = []
    worm_logTimeFormat.restype = c_char_p

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 363
if _libs["libWormAPI"].has("worm_init", "cdecl"):
    worm_init = _libs["libWormAPI"].get("worm_init", "cdecl")
    worm_init.argtypes = [POINTER(POINTER(WormContext)), String]
    worm_init.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 389
for _lib in _libs.values():
    if not _lib.has("worm_init_lan", "cdecl"):
        continue
    worm_init_lan = _lib.get("worm_init_lan", "cdecl")
    worm_init_lan.argtypes = [POINTER(POINTER(WormContext)), String, String]
    worm_init_lan.restype = WormError
    break

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 433
if _libs["libWormAPI"].has("worm_keepalive_configure", "cdecl"):
    worm_keepalive_configure = _libs["libWormAPI"].get(
        "worm_keepalive_configure", "cdecl"
    )
    worm_keepalive_configure.argtypes = [POINTER(WormContext), c_int]
    worm_keepalive_configure.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 446
if _libs["libWormAPI"].has("worm_keepalive_disable", "cdecl"):
    worm_keepalive_disable = _libs["libWormAPI"].get("worm_keepalive_disable", "cdecl")
    worm_keepalive_disable.argtypes = [POINTER(WormContext)]
    worm_keepalive_disable.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 475
for _lib in _libs.values():
    if not _lib.has("worm_lantse_select", "cdecl"):
        continue
    worm_lantse_select = _lib.get("worm_lantse_select", "cdecl")
    worm_lantse_select.argtypes = [POINTER(WormContext), POINTER(c_ubyte), c_int]
    worm_lantse_select.restype = WormError
    break

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 541
for _lib in _libs.values():
    if not _lib.has("worm_lantse_lock", "cdecl"):
        continue
    worm_lantse_lock = _lib.get("worm_lantse_lock", "cdecl")
    worm_lantse_lock.argtypes = [POINTER(WormContext)]
    worm_lantse_lock.restype = WormError
    break

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 553
for _lib in _libs.values():
    if not _lib.has("worm_lantse_unlock", "cdecl"):
        continue
    worm_lantse_unlock = _lib.get("worm_lantse_unlock", "cdecl")
    worm_lantse_unlock.argtypes = [POINTER(WormContext)]
    worm_lantse_unlock.restype = WormError
    break

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 562
if _libs["libWormAPI"].has("worm_cleanup", "cdecl"):
    worm_cleanup = _libs["libWormAPI"].get("worm_cleanup", "cdecl")
    worm_cleanup.argtypes = [POINTER(WormContext)]
    worm_cleanup.restype = WormError


# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 597
class struct_WormInfo(Structure):
    pass


WormInfo = struct_WormInfo  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 597

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 608
if _libs["libWormAPI"].has("worm_info_new", "cdecl"):
    worm_info_new = _libs["libWormAPI"].get("worm_info_new", "cdecl")
    worm_info_new.argtypes = [POINTER(WormContext)]
    worm_info_new.restype = POINTER(WormInfo)

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 617
if _libs["libWormAPI"].has("worm_info_free", "cdecl"):
    worm_info_free = _libs["libWormAPI"].get("worm_info_free", "cdecl")
    worm_info_free.argtypes = [POINTER(WormInfo)]
    worm_info_free.restype = None

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 626
if _libs["libWormAPI"].has("worm_info_read", "cdecl"):
    worm_info_read = _libs["libWormAPI"].get("worm_info_read", "cdecl")
    worm_info_read.argtypes = [POINTER(WormInfo)]
    worm_info_read.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 637
if _libs["libWormAPI"].has("worm_info_customizationIdentifier", "cdecl"):
    worm_info_customizationIdentifier = _libs["libWormAPI"].get(
        "worm_info_customizationIdentifier", "cdecl"
    )
    worm_info_customizationIdentifier.argtypes = [
        POINTER(WormInfo),
        POINTER(POINTER(c_ubyte)),
        POINTER(c_int),
    ]
    worm_info_customizationIdentifier.restype = None

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 641
if _libs["libWormAPI"].has("worm_info_uniqueId", "cdecl"):
    worm_info_uniqueId = _libs["libWormAPI"].get("worm_info_uniqueId", "cdecl")
    worm_info_uniqueId.argtypes = [
        POINTER(WormInfo),
        POINTER(POINTER(c_ubyte)),
        POINTER(c_int),
    ]
    worm_info_uniqueId.restype = None

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 649
if _libs["libWormAPI"].has("worm_info_isDevelopmentFirmware", "cdecl"):
    worm_info_isDevelopmentFirmware = _libs["libWormAPI"].get(
        "worm_info_isDevelopmentFirmware", "cdecl"
    )
    worm_info_isDevelopmentFirmware.argtypes = [POINTER(WormInfo)]
    worm_info_isDevelopmentFirmware.restype = c_int

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 656
if _libs["libWormAPI"].has("worm_info_capacity", "cdecl"):
    worm_info_capacity = _libs["libWormAPI"].get("worm_info_capacity", "cdecl")
    worm_info_capacity.argtypes = [POINTER(WormInfo)]
    worm_info_capacity.restype = uint32_t

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 665
if _libs["libWormAPI"].has("worm_info_size", "cdecl"):
    worm_info_size = _libs["libWormAPI"].get("worm_info_size", "cdecl")
    worm_info_size.argtypes = [POINTER(WormInfo)]
    worm_info_size.restype = uint32_t

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 668
if _libs["libWormAPI"].has("worm_info_isStoreOpen", "cdecl"):
    worm_info_isStoreOpen = _libs["libWormAPI"].get("worm_info_isStoreOpen", "cdecl")
    worm_info_isStoreOpen.argtypes = [POINTER(WormInfo)]
    worm_info_isStoreOpen.restype = c_int

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 676
if _libs["libWormAPI"].has("worm_info_hasValidTime", "cdecl"):
    worm_info_hasValidTime = _libs["libWormAPI"].get("worm_info_hasValidTime", "cdecl")
    worm_info_hasValidTime.argtypes = [POINTER(WormInfo)]
    worm_info_hasValidTime.restype = c_int

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 684
if _libs["libWormAPI"].has("worm_info_hasPassedSelfTest", "cdecl"):
    worm_info_hasPassedSelfTest = _libs["libWormAPI"].get(
        "worm_info_hasPassedSelfTest", "cdecl"
    )
    worm_info_hasPassedSelfTest.argtypes = [POINTER(WormInfo)]
    worm_info_hasPassedSelfTest.restype = c_int

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 696
if _libs["libWormAPI"].has("worm_info_isCtssInterfaceActive", "cdecl"):
    worm_info_isCtssInterfaceActive = _libs["libWormAPI"].get(
        "worm_info_isCtssInterfaceActive", "cdecl"
    )
    worm_info_isCtssInterfaceActive.argtypes = [POINTER(WormInfo)]
    worm_info_isCtssInterfaceActive.restype = c_int

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 700
if _libs["libWormAPI"].has("worm_info_isErsInterfaceActive", "cdecl"):
    worm_info_isErsInterfaceActive = _libs["libWormAPI"].get(
        "worm_info_isErsInterfaceActive", "cdecl"
    )
    worm_info_isErsInterfaceActive.argtypes = [POINTER(WormInfo)]
    worm_info_isErsInterfaceActive.restype = c_int

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 710
if _libs["libWormAPI"].has("worm_info_isExportEnabledIfCspTestFails", "cdecl"):
    worm_info_isExportEnabledIfCspTestFails = _libs["libWormAPI"].get(
        "worm_info_isExportEnabledIfCspTestFails", "cdecl"
    )
    worm_info_isExportEnabledIfCspTestFails.argtypes = [POINTER(WormInfo)]
    worm_info_isExportEnabledIfCspTestFails.restype = c_int

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 719
if _libs["libWormAPI"].has("worm_info_initializationState", "cdecl"):
    worm_info_initializationState = _libs["libWormAPI"].get(
        "worm_info_initializationState", "cdecl"
    )
    worm_info_initializationState.argtypes = [POINTER(WormInfo)]
    worm_info_initializationState.restype = WormInitializationState

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 726
if _libs["libWormAPI"].has("worm_info_isDataImportInProgress", "cdecl"):
    worm_info_isDataImportInProgress = _libs["libWormAPI"].get(
        "worm_info_isDataImportInProgress", "cdecl"
    )
    worm_info_isDataImportInProgress.argtypes = [POINTER(WormInfo)]
    worm_info_isDataImportInProgress.restype = c_int

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 730
if _libs["libWormAPI"].has("worm_info_isTransactionInProgress", "cdecl"):
    worm_info_isTransactionInProgress = _libs["libWormAPI"].get(
        "worm_info_isTransactionInProgress", "cdecl"
    )
    worm_info_isTransactionInProgress.argtypes = [POINTER(WormInfo)]
    worm_info_isTransactionInProgress.restype = c_int

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 736
if _libs["libWormAPI"].has("worm_info_hasChangedPuk", "cdecl"):
    worm_info_hasChangedPuk = _libs["libWormAPI"].get(
        "worm_info_hasChangedPuk", "cdecl"
    )
    worm_info_hasChangedPuk.argtypes = [POINTER(WormInfo)]
    worm_info_hasChangedPuk.restype = c_int

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 742
if _libs["libWormAPI"].has("worm_info_hasChangedAdminPin", "cdecl"):
    worm_info_hasChangedAdminPin = _libs["libWormAPI"].get(
        "worm_info_hasChangedAdminPin", "cdecl"
    )
    worm_info_hasChangedAdminPin.argtypes = [POINTER(WormInfo)]
    worm_info_hasChangedAdminPin.restype = c_int

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 748
if _libs["libWormAPI"].has("worm_info_hasChangedTimeAdminPin", "cdecl"):
    worm_info_hasChangedTimeAdminPin = _libs["libWormAPI"].get(
        "worm_info_hasChangedTimeAdminPin", "cdecl"
    )
    worm_info_hasChangedTimeAdminPin.argtypes = [POINTER(WormInfo)]
    worm_info_hasChangedTimeAdminPin.restype = c_int

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 752
if _libs["libWormAPI"].has("worm_info_firmwareVersion", "cdecl"):
    worm_info_firmwareVersion = _libs["libWormAPI"].get(
        "worm_info_firmwareVersion", "cdecl"
    )
    worm_info_firmwareVersion.argtypes = [POINTER(WormInfo)]
    worm_info_firmwareVersion.restype = uint32_t

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 764
if _libs["libWormAPI"].has("worm_info_timeUntilNextSelfTest", "cdecl"):
    worm_info_timeUntilNextSelfTest = _libs["libWormAPI"].get(
        "worm_info_timeUntilNextSelfTest", "cdecl"
    )
    worm_info_timeUntilNextSelfTest.argtypes = [POINTER(WormInfo)]
    worm_info_timeUntilNextSelfTest.restype = uint32_t

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 780
if _libs["libWormAPI"].has("worm_info_startedTransactions", "cdecl"):
    worm_info_startedTransactions = _libs["libWormAPI"].get(
        "worm_info_startedTransactions", "cdecl"
    )
    worm_info_startedTransactions.argtypes = [POINTER(WormInfo)]
    worm_info_startedTransactions.restype = uint32_t

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 789
if _libs["libWormAPI"].has("worm_info_maxStartedTransactions", "cdecl"):
    worm_info_maxStartedTransactions = _libs["libWormAPI"].get(
        "worm_info_maxStartedTransactions", "cdecl"
    )
    worm_info_maxStartedTransactions.argtypes = [POINTER(WormInfo)]
    worm_info_maxStartedTransactions.restype = uint32_t

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 801
if _libs["libWormAPI"].has("worm_info_createdSignatures", "cdecl"):
    worm_info_createdSignatures = _libs["libWormAPI"].get(
        "worm_info_createdSignatures", "cdecl"
    )
    worm_info_createdSignatures.argtypes = [POINTER(WormInfo)]
    worm_info_createdSignatures.restype = uint32_t

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 809
if _libs["libWormAPI"].has("worm_info_maxSignatures", "cdecl"):
    worm_info_maxSignatures = _libs["libWormAPI"].get(
        "worm_info_maxSignatures", "cdecl"
    )
    worm_info_maxSignatures.argtypes = [POINTER(WormInfo)]
    worm_info_maxSignatures.restype = uint32_t

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 821
if _libs["libWormAPI"].has("worm_info_remainingSignatures", "cdecl"):
    worm_info_remainingSignatures = _libs["libWormAPI"].get(
        "worm_info_remainingSignatures", "cdecl"
    )
    worm_info_remainingSignatures.argtypes = [POINTER(WormInfo)]
    worm_info_remainingSignatures.restype = uint32_t

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 831
if _libs["libWormAPI"].has("worm_info_maxTimeSynchronizationDelay", "cdecl"):
    worm_info_maxTimeSynchronizationDelay = _libs["libWormAPI"].get(
        "worm_info_maxTimeSynchronizationDelay", "cdecl"
    )
    worm_info_maxTimeSynchronizationDelay.argtypes = [POINTER(WormInfo)]
    worm_info_maxTimeSynchronizationDelay.restype = uint32_t

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 843
if _libs["libWormAPI"].has("worm_info_maxUpdateDelay", "cdecl"):
    worm_info_maxUpdateDelay = _libs["libWormAPI"].get(
        "worm_info_maxUpdateDelay", "cdecl"
    )
    worm_info_maxUpdateDelay.argtypes = [POINTER(WormInfo)]
    worm_info_maxUpdateDelay.restype = uint32_t

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 862
if _libs["libWormAPI"].has("worm_info_tsePublicKey", "cdecl"):
    worm_info_tsePublicKey = _libs["libWormAPI"].get("worm_info_tsePublicKey", "cdecl")
    worm_info_tsePublicKey.argtypes = [
        POINTER(WormInfo),
        POINTER(POINTER(c_ubyte)),
        POINTER(worm_uint),
    ]
    worm_info_tsePublicKey.restype = None

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 886
if _libs["libWormAPI"].has("worm_info_timeUntilNextTimeSynchronization", "cdecl"):
    worm_info_timeUntilNextTimeSynchronization = _libs["libWormAPI"].get(
        "worm_info_timeUntilNextTimeSynchronization", "cdecl"
    )
    worm_info_timeUntilNextTimeSynchronization.argtypes = [POINTER(WormInfo)]
    worm_info_timeUntilNextTimeSynchronization.restype = uint32_t

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 899
if _libs["libWormAPI"].has("worm_info_tseSerialNumber", "cdecl"):
    worm_info_tseSerialNumber = _libs["libWormAPI"].get(
        "worm_info_tseSerialNumber", "cdecl"
    )
    worm_info_tseSerialNumber.argtypes = [
        POINTER(WormInfo),
        POINTER(POINTER(c_ubyte)),
        POINTER(worm_uint),
    ]
    worm_info_tseSerialNumber.restype = None

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 915
if _libs["libWormAPI"].has("worm_info_tseDescription", "cdecl"):
    worm_info_tseDescription = _libs["libWormAPI"].get(
        "worm_info_tseDescription", "cdecl"
    )
    worm_info_tseDescription.argtypes = [POINTER(WormInfo)]
    worm_info_tseDescription.restype = c_char_p

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 923
if _libs["libWormAPI"].has("worm_info_registeredClients", "cdecl"):
    worm_info_registeredClients = _libs["libWormAPI"].get(
        "worm_info_registeredClients", "cdecl"
    )
    worm_info_registeredClients.argtypes = [POINTER(WormInfo)]
    worm_info_registeredClients.restype = uint32_t

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 932
if _libs["libWormAPI"].has("worm_info_maxRegisteredClients", "cdecl"):
    worm_info_maxRegisteredClients = _libs["libWormAPI"].get(
        "worm_info_maxRegisteredClients", "cdecl"
    )
    worm_info_maxRegisteredClients.argtypes = [POINTER(WormInfo)]
    worm_info_maxRegisteredClients.restype = uint32_t

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 945
if _libs["libWormAPI"].has("worm_info_certificateExpirationDate", "cdecl"):
    worm_info_certificateExpirationDate = _libs["libWormAPI"].get(
        "worm_info_certificateExpirationDate", "cdecl"
    )
    worm_info_certificateExpirationDate.argtypes = [POINTER(WormInfo)]
    worm_info_certificateExpirationDate.restype = worm_uint

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 958
if _libs["libWormAPI"].has("worm_info_tarExportSizeInSectors", "cdecl"):
    worm_info_tarExportSizeInSectors = _libs["libWormAPI"].get(
        "worm_info_tarExportSizeInSectors", "cdecl"
    )
    worm_info_tarExportSizeInSectors.argtypes = [POINTER(WormInfo)]
    worm_info_tarExportSizeInSectors.restype = worm_uint

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 971
if _libs["libWormAPI"].has("worm_info_tarExportSize", "cdecl"):
    worm_info_tarExportSize = _libs["libWormAPI"].get(
        "worm_info_tarExportSize", "cdecl"
    )
    worm_info_tarExportSize.argtypes = [POINTER(WormInfo)]
    worm_info_tarExportSize.restype = uint64_t

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 984
if _libs["libWormAPI"].has("worm_info_hardwareVersion", "cdecl"):
    worm_info_hardwareVersion = _libs["libWormAPI"].get(
        "worm_info_hardwareVersion", "cdecl"
    )
    worm_info_hardwareVersion.argtypes = [POINTER(WormInfo)]
    worm_info_hardwareVersion.restype = uint32_t

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 996
if _libs["libWormAPI"].has("worm_info_softwareVersion", "cdecl"):
    worm_info_softwareVersion = _libs["libWormAPI"].get(
        "worm_info_softwareVersion", "cdecl"
    )
    worm_info_softwareVersion.argtypes = [POINTER(WormInfo)]
    worm_info_softwareVersion.restype = uint32_t

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1005
if _libs["libWormAPI"].has("worm_info_formFactor", "cdecl"):
    worm_info_formFactor = _libs["libWormAPI"].get("worm_info_formFactor", "cdecl")
    worm_info_formFactor.argtypes = [POINTER(WormInfo)]
    worm_info_formFactor.restype = c_char_p

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1070
if _libs["libWormAPI"].has("worm_flash_health_summary", "cdecl"):
    worm_flash_health_summary = _libs["libWormAPI"].get(
        "worm_flash_health_summary", "cdecl"
    )
    worm_flash_health_summary.argtypes = [
        POINTER(WormContext),
        POINTER(uint32_t),
        POINTER(uint8_t),
        POINTER(uint8_t),
        POINTER(uint8_t),
    ]
    worm_flash_health_summary.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1087
if _libs["libWormAPI"].has("worm_flash_health_needs_replacement", "cdecl"):
    worm_flash_health_needs_replacement = _libs["libWormAPI"].get(
        "worm_flash_health_needs_replacement", "cdecl"
    )
    worm_flash_health_needs_replacement.argtypes = [uint32_t, uint8_t, uint8_t]
    worm_flash_health_needs_replacement.restype = c_int

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1140
if _libs["libWormAPI"].has("worm_tse_factoryReset", "cdecl"):
    worm_tse_factoryReset = _libs["libWormAPI"].get("worm_tse_factoryReset", "cdecl")
    worm_tse_factoryReset.argtypes = [POINTER(WormContext)]
    worm_tse_factoryReset.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1190
if _libs["libWormAPI"].has("worm_tse_setup", "cdecl"):
    worm_tse_setup = _libs["libWormAPI"].get("worm_tse_setup", "cdecl")
    worm_tse_setup.argtypes = [
        POINTER(WormContext),
        POINTER(c_ubyte),
        c_int,
        POINTER(c_ubyte),
        c_int,
        POINTER(c_ubyte),
        c_int,
        POINTER(c_ubyte),
        c_int,
        String,
    ]
    worm_tse_setup.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1209
if _libs["libWormAPI"].has("worm_tse_ctss_enable", "cdecl"):
    worm_tse_ctss_enable = _libs["libWormAPI"].get("worm_tse_ctss_enable", "cdecl")
    worm_tse_ctss_enable.argtypes = [POINTER(WormContext)]
    worm_tse_ctss_enable.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1213
if _libs["libWormAPI"].has("worm_tse_ers_enable", "cdecl"):
    worm_tse_ers_enable = _libs["libWormAPI"].get("worm_tse_ers_enable", "cdecl")
    worm_tse_ers_enable.argtypes = [POINTER(WormContext)]
    worm_tse_ers_enable.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1227
if _libs["libWormAPI"].has("worm_tse_ctss_disable", "cdecl"):
    worm_tse_ctss_disable = _libs["libWormAPI"].get("worm_tse_ctss_disable", "cdecl")
    worm_tse_ctss_disable.argtypes = [POINTER(WormContext)]
    worm_tse_ctss_disable.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1231
if _libs["libWormAPI"].has("worm_tse_ers_disable", "cdecl"):
    worm_tse_ers_disable = _libs["libWormAPI"].get("worm_tse_ers_disable", "cdecl")
    worm_tse_ers_disable.argtypes = [POINTER(WormContext)]
    worm_tse_ers_disable.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1242
if _libs["libWormAPI"].has("worm_tse_initialize", "cdecl"):
    worm_tse_initialize = _libs["libWormAPI"].get("worm_tse_initialize", "cdecl")
    worm_tse_initialize.argtypes = [POINTER(WormContext)]
    worm_tse_initialize.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1259
if _libs["libWormAPI"].has("worm_tse_decommission", "cdecl"):
    worm_tse_decommission = _libs["libWormAPI"].get("worm_tse_decommission", "cdecl")
    worm_tse_decommission.argtypes = [POINTER(WormContext)]
    worm_tse_decommission.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1298
if _libs["libWormAPI"].has("worm_tse_updateTime", "cdecl"):
    worm_tse_updateTime = _libs["libWormAPI"].get("worm_tse_updateTime", "cdecl")
    worm_tse_updateTime.argtypes = [POINTER(WormContext), worm_uint]
    worm_tse_updateTime.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1337
if _libs["libWormAPI"].has("worm_tse_firmwareUpdate_check", "cdecl"):
    worm_tse_firmwareUpdate_check = _libs["libWormAPI"].get(
        "worm_tse_firmwareUpdate_check", "cdecl"
    )
    worm_tse_firmwareUpdate_check.argtypes = [
        POINTER(WormContext),
        POINTER(c_int),
        String,
        c_int,
    ]
    worm_tse_firmwareUpdate_check.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1358
if _libs["libWormAPI"].has("worm_tse_firmwareUpdate_isBundledAvailable", "cdecl"):
    worm_tse_firmwareUpdate_isBundledAvailable = _libs["libWormAPI"].get(
        "worm_tse_firmwareUpdate_isBundledAvailable", "cdecl"
    )
    worm_tse_firmwareUpdate_isBundledAvailable.argtypes = [
        POINTER(WormContext),
        POINTER(WormTseFirmwareUpdate),
    ]
    worm_tse_firmwareUpdate_isBundledAvailable.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1388
if _libs["libWormAPI"].has("worm_tse_firmwareUpdate_applyBundled", "cdecl"):
    worm_tse_firmwareUpdate_applyBundled = _libs["libWormAPI"].get(
        "worm_tse_firmwareUpdate_applyBundled", "cdecl"
    )
    worm_tse_firmwareUpdate_applyBundled.argtypes = [POINTER(WormContext)]
    worm_tse_firmwareUpdate_applyBundled.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1407
if _libs["libWormAPI"].has("worm_tse_firmwareUpdate_transfer", "cdecl"):
    worm_tse_firmwareUpdate_transfer = _libs["libWormAPI"].get(
        "worm_tse_firmwareUpdate_transfer", "cdecl"
    )
    worm_tse_firmwareUpdate_transfer.argtypes = [
        POINTER(WormContext),
        uint32_t,
        POINTER(c_ubyte),
        c_int,
    ]
    worm_tse_firmwareUpdate_transfer.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1447
if _libs["libWormAPI"].has("worm_tse_firmwareUpdate_apply", "cdecl"):
    worm_tse_firmwareUpdate_apply = _libs["libWormAPI"].get(
        "worm_tse_firmwareUpdate_apply", "cdecl"
    )
    worm_tse_firmwareUpdate_apply.argtypes = [POINTER(WormContext), uint32_t]
    worm_tse_firmwareUpdate_apply.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1476
if _libs["libWormAPI"].has("worm_tse_enableExportIfCspTestFails", "cdecl"):
    worm_tse_enableExportIfCspTestFails = _libs["libWormAPI"].get(
        "worm_tse_enableExportIfCspTestFails", "cdecl"
    )
    worm_tse_enableExportIfCspTestFails.argtypes = [POINTER(WormContext)]
    worm_tse_enableExportIfCspTestFails.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1502
if _libs["libWormAPI"].has("worm_tse_disableExportIfCspTestFails", "cdecl"):
    worm_tse_disableExportIfCspTestFails = _libs["libWormAPI"].get(
        "worm_tse_disableExportIfCspTestFails", "cdecl"
    )
    worm_tse_disableExportIfCspTestFails.argtypes = [POINTER(WormContext)]
    worm_tse_disableExportIfCspTestFails.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1537
if _libs["libWormAPI"].has("worm_tse_runSelfTest", "cdecl"):
    worm_tse_runSelfTest = _libs["libWormAPI"].get("worm_tse_runSelfTest", "cdecl")
    worm_tse_runSelfTest.argtypes = [POINTER(WormContext), String]
    worm_tse_runSelfTest.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1553
if _libs["libWormAPI"].has("worm_tse_registerClient", "cdecl"):
    worm_tse_registerClient = _libs["libWormAPI"].get(
        "worm_tse_registerClient", "cdecl"
    )
    worm_tse_registerClient.argtypes = [POINTER(WormContext), String]
    worm_tse_registerClient.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1569
if _libs["libWormAPI"].has("worm_tse_deregisterClient", "cdecl"):
    worm_tse_deregisterClient = _libs["libWormAPI"].get(
        "worm_tse_deregisterClient", "cdecl"
    )
    worm_tse_deregisterClient.argtypes = [POINTER(WormContext), String]
    worm_tse_deregisterClient.restype = WormError


# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1578
class struct_anon_7(Structure):
    pass


struct_anon_7.__slots__ = [
    "amount",
    "clientIds",
]
struct_anon_7._fields_ = [
    ("amount", c_int),
    ("clientIds", (c_char * int(31)) * int(16)),
]

WormRegisteredClients = struct_anon_7  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1578

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1597
if _libs["libWormAPI"].has("worm_tse_listRegisteredClients", "cdecl"):
    worm_tse_listRegisteredClients = _libs["libWormAPI"].get(
        "worm_tse_listRegisteredClients", "cdecl"
    )
    worm_tse_listRegisteredClients.argtypes = [
        POINTER(WormContext),
        c_int,
        POINTER(WormRegisteredClients),
    ]
    worm_tse_listRegisteredClients.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1657
if _libs["libWormAPI"].has("worm_user_login", "cdecl"):
    worm_user_login = _libs["libWormAPI"].get("worm_user_login", "cdecl")
    worm_user_login.argtypes = [
        POINTER(WormContext),
        WormUserId,
        POINTER(c_ubyte),
        c_int,
        POINTER(c_int),
    ]
    worm_user_login.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1670
if _libs["libWormAPI"].has("worm_user_logout", "cdecl"):
    worm_user_logout = _libs["libWormAPI"].get("worm_user_logout", "cdecl")
    worm_user_logout.argtypes = [POINTER(WormContext), WormUserId]
    worm_user_logout.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1688
if _libs["libWormAPI"].has("worm_user_unblock", "cdecl"):
    worm_user_unblock = _libs["libWormAPI"].get("worm_user_unblock", "cdecl")
    worm_user_unblock.argtypes = [
        POINTER(WormContext),
        WormUserId,
        POINTER(c_ubyte),
        c_int,
        POINTER(c_ubyte),
        c_int,
        POINTER(c_int),
    ]
    worm_user_unblock.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1708
if _libs["libWormAPI"].has("worm_user_change_puk", "cdecl"):
    worm_user_change_puk = _libs["libWormAPI"].get("worm_user_change_puk", "cdecl")
    worm_user_change_puk.argtypes = [
        POINTER(WormContext),
        POINTER(c_ubyte),
        c_int,
        POINTER(c_ubyte),
        c_int,
        POINTER(c_int),
    ]
    worm_user_change_puk.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1727
if _libs["libWormAPI"].has("worm_user_change_pin", "cdecl"):
    worm_user_change_pin = _libs["libWormAPI"].get("worm_user_change_pin", "cdecl")
    worm_user_change_pin.argtypes = [
        POINTER(WormContext),
        WormUserId,
        POINTER(c_ubyte),
        c_int,
        POINTER(c_ubyte),
        c_int,
        POINTER(c_int),
    ]
    worm_user_change_pin.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1753
if _libs["libWormAPI"].has("worm_user_deriveInitialCredentials", "cdecl"):
    worm_user_deriveInitialCredentials = _libs["libWormAPI"].get(
        "worm_user_deriveInitialCredentials", "cdecl"
    )
    worm_user_deriveInitialCredentials.argtypes = [
        POINTER(WormContext),
        POINTER(c_ubyte),
        c_int,
        POINTER(c_ubyte),
        c_int,
        POINTER(c_ubyte),
        c_int,
        POINTER(c_ubyte),
        c_int,
    ]
    worm_user_deriveInitialCredentials.restype = WormError


# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1804
class struct_WormTransactionResponse(Structure):
    pass


WormTransactionResponse = struct_WormTransactionResponse  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1804

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1808
if _libs["libWormAPI"].has("worm_transaction_openStore", "cdecl"):
    worm_transaction_openStore = _libs["libWormAPI"].get(
        "worm_transaction_openStore", "cdecl"
    )
    worm_transaction_openStore.argtypes = [POINTER(WormContext), worm_uint]
    worm_transaction_openStore.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1827
if _libs["libWormAPI"].has("worm_transaction_start", "cdecl"):
    worm_transaction_start = _libs["libWormAPI"].get("worm_transaction_start", "cdecl")
    worm_transaction_start.argtypes = [
        POINTER(WormContext),
        String,
        POINTER(c_ubyte),
        worm_uint,
        String,
        POINTER(WormTransactionResponse),
    ]
    worm_transaction_start.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1853
if _libs["libWormAPI"].has("worm_transaction_update", "cdecl"):
    worm_transaction_update = _libs["libWormAPI"].get(
        "worm_transaction_update", "cdecl"
    )
    worm_transaction_update.argtypes = [
        POINTER(WormContext),
        String,
        worm_uint,
        POINTER(c_ubyte),
        worm_uint,
        String,
        POINTER(WormTransactionResponse),
    ]
    worm_transaction_update.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1878
if _libs["libWormAPI"].has("worm_transaction_finish", "cdecl"):
    worm_transaction_finish = _libs["libWormAPI"].get(
        "worm_transaction_finish", "cdecl"
    )
    worm_transaction_finish.argtypes = [
        POINTER(WormContext),
        String,
        worm_uint,
        POINTER(c_ubyte),
        worm_uint,
        String,
        POINTER(WormTransactionResponse),
    ]
    worm_transaction_finish.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1898
if _libs["libWormAPI"].has("worm_transaction_lastResponse", "cdecl"):
    worm_transaction_lastResponse = _libs["libWormAPI"].get(
        "worm_transaction_lastResponse", "cdecl"
    )
    worm_transaction_lastResponse.argtypes = [
        POINTER(WormContext),
        String,
        POINTER(WormTransactionResponse),
    ]
    worm_transaction_lastResponse.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1925
if _libs["libWormAPI"].has("worm_transaction_listStartedTransactions", "cdecl"):
    worm_transaction_listStartedTransactions = _libs["libWormAPI"].get(
        "worm_transaction_listStartedTransactions", "cdecl"
    )
    worm_transaction_listStartedTransactions.argtypes = [
        POINTER(WormContext),
        String,
        c_int,
        POINTER(worm_uint),
        c_int,
        POINTER(c_int),
    ]
    worm_transaction_listStartedTransactions.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1940
if _libs["libWormAPI"].has("worm_transaction_response_new", "cdecl"):
    worm_transaction_response_new = _libs["libWormAPI"].get(
        "worm_transaction_response_new", "cdecl"
    )
    worm_transaction_response_new.argtypes = [POINTER(WormContext)]
    worm_transaction_response_new.restype = POINTER(WormTransactionResponse)

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1951
if _libs["libWormAPI"].has("worm_transaction_response_free", "cdecl"):
    worm_transaction_response_free = _libs["libWormAPI"].get(
        "worm_transaction_response_free", "cdecl"
    )
    worm_transaction_response_free.argtypes = [POINTER(WormTransactionResponse)]
    worm_transaction_response_free.restype = None

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1962
if _libs["libWormAPI"].has("worm_transaction_response_logTime", "cdecl"):
    worm_transaction_response_logTime = _libs["libWormAPI"].get(
        "worm_transaction_response_logTime", "cdecl"
    )
    worm_transaction_response_logTime.argtypes = [POINTER(WormTransactionResponse)]
    worm_transaction_response_logTime.restype = worm_uint

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1976
if _libs["libWormAPI"].has("worm_transaction_response_serialNumber", "cdecl"):
    worm_transaction_response_serialNumber = _libs["libWormAPI"].get(
        "worm_transaction_response_serialNumber", "cdecl"
    )
    worm_transaction_response_serialNumber.argtypes = [
        POINTER(WormTransactionResponse),
        POINTER(POINTER(c_ubyte)),
        POINTER(worm_uint),
    ]
    worm_transaction_response_serialNumber.restype = None

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1988
if _libs["libWormAPI"].has("worm_transaction_response_signatureCounter", "cdecl"):
    worm_transaction_response_signatureCounter = _libs["libWormAPI"].get(
        "worm_transaction_response_signatureCounter", "cdecl"
    )
    worm_transaction_response_signatureCounter.argtypes = [
        POINTER(WormTransactionResponse)
    ]
    worm_transaction_response_signatureCounter.restype = worm_uint

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 2001
if _libs["libWormAPI"].has("worm_transaction_response_signature", "cdecl"):
    worm_transaction_response_signature = _libs["libWormAPI"].get(
        "worm_transaction_response_signature", "cdecl"
    )
    worm_transaction_response_signature.argtypes = [
        POINTER(WormTransactionResponse),
        POINTER(POINTER(c_ubyte)),
        POINTER(worm_uint),
    ]
    worm_transaction_response_signature.restype = None

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 2015
if _libs["libWormAPI"].has("worm_transaction_response_transactionNumber", "cdecl"):
    worm_transaction_response_transactionNumber = _libs["libWormAPI"].get(
        "worm_transaction_response_transactionNumber", "cdecl"
    )
    worm_transaction_response_transactionNumber.argtypes = [
        POINTER(WormTransactionResponse)
    ]
    worm_transaction_response_transactionNumber.restype = worm_uint


# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 2051
class struct_WormEntry(Structure):
    pass


WormEntry = struct_WormEntry  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 2051

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 2062
if _libs["libWormAPI"].has("worm_entry_new", "cdecl"):
    worm_entry_new = _libs["libWormAPI"].get("worm_entry_new", "cdecl")
    worm_entry_new.argtypes = [POINTER(WormContext)]
    worm_entry_new.restype = POINTER(WormEntry)

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 2071
if _libs["libWormAPI"].has("worm_entry_free", "cdecl"):
    worm_entry_free = _libs["libWormAPI"].get("worm_entry_free", "cdecl")
    worm_entry_free.argtypes = [POINTER(WormEntry)]
    worm_entry_free.restype = None

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 2086
if _libs["libWormAPI"].has("worm_entry_iterate_first", "cdecl"):
    worm_entry_iterate_first = _libs["libWormAPI"].get(
        "worm_entry_iterate_first", "cdecl"
    )
    worm_entry_iterate_first.argtypes = [POINTER(WormEntry)]
    worm_entry_iterate_first.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 2101
if _libs["libWormAPI"].has("worm_entry_iterate_last", "cdecl"):
    worm_entry_iterate_last = _libs["libWormAPI"].get(
        "worm_entry_iterate_last", "cdecl"
    )
    worm_entry_iterate_last.argtypes = [POINTER(WormEntry)]
    worm_entry_iterate_last.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 2117
if _libs["libWormAPI"].has("worm_entry_iterate_id", "cdecl"):
    worm_entry_iterate_id = _libs["libWormAPI"].get("worm_entry_iterate_id", "cdecl")
    worm_entry_iterate_id.argtypes = [POINTER(WormEntry), uint32_t]
    worm_entry_iterate_id.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 2129
if _libs["libWormAPI"].has("worm_entry_iterate_next", "cdecl"):
    worm_entry_iterate_next = _libs["libWormAPI"].get(
        "worm_entry_iterate_next", "cdecl"
    )
    worm_entry_iterate_next.argtypes = [POINTER(WormEntry)]
    worm_entry_iterate_next.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 2139
if _libs["libWormAPI"].has("worm_entry_isValid", "cdecl"):
    worm_entry_isValid = _libs["libWormAPI"].get("worm_entry_isValid", "cdecl")
    worm_entry_isValid.argtypes = [POINTER(WormEntry)]
    worm_entry_isValid.restype = c_int

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 2157
if _libs["libWormAPI"].has("worm_entry_id", "cdecl"):
    worm_entry_id = _libs["libWormAPI"].get("worm_entry_id", "cdecl")
    worm_entry_id.argtypes = [POINTER(WormEntry)]
    worm_entry_id.restype = uint32_t

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 2164
if _libs["libWormAPI"].has("worm_entry_type", "cdecl"):
    worm_entry_type = _libs["libWormAPI"].get("worm_entry_type", "cdecl")
    worm_entry_type.argtypes = [POINTER(WormEntry)]
    worm_entry_type.restype = WormEntryType

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 2176
if _libs["libWormAPI"].has("worm_entry_logMessageLength", "cdecl"):
    worm_entry_logMessageLength = _libs["libWormAPI"].get(
        "worm_entry_logMessageLength", "cdecl"
    )
    worm_entry_logMessageLength.argtypes = [POINTER(WormEntry)]
    worm_entry_logMessageLength.restype = worm_uint

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 2187
if _libs["libWormAPI"].has("worm_entry_readLogMessage", "cdecl"):
    worm_entry_readLogMessage = _libs["libWormAPI"].get(
        "worm_entry_readLogMessage", "cdecl"
    )
    worm_entry_readLogMessage.argtypes = [
        POINTER(WormEntry),
        POINTER(c_ubyte),
        worm_uint,
    ]
    worm_entry_readLogMessage.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 2197
if _libs["libWormAPI"].has("worm_entry_processDataLength", "cdecl"):
    worm_entry_processDataLength = _libs["libWormAPI"].get(
        "worm_entry_processDataLength", "cdecl"
    )
    worm_entry_processDataLength.argtypes = [POINTER(WormEntry)]
    worm_entry_processDataLength.restype = worm_uint

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 2212
if _libs["libWormAPI"].has("worm_entry_readProcessData", "cdecl"):
    worm_entry_readProcessData = _libs["libWormAPI"].get(
        "worm_entry_readProcessData", "cdecl"
    )
    worm_entry_readProcessData.argtypes = [
        POINTER(WormEntry),
        worm_uint,
        POINTER(c_ubyte),
        worm_uint,
    ]
    worm_entry_readProcessData.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 2243
if _libs["libWormAPI"].has("worm_getLogMessageCertificate", "cdecl"):
    worm_getLogMessageCertificate = _libs["libWormAPI"].get(
        "worm_getLogMessageCertificate", "cdecl"
    )
    worm_getLogMessageCertificate.argtypes = [
        POINTER(WormContext),
        POINTER(c_ubyte),
        POINTER(uint32_t),
    ]
    worm_getLogMessageCertificate.restype = WormError

WormExportTarCallback = CFUNCTYPE(
    UNCHECKED(c_int), POINTER(c_ubyte), c_uint, POINTER(None)
)  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 2257

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 2281
if _libs["libWormAPI"].has("worm_export_tar", "cdecl"):
    worm_export_tar = _libs["libWormAPI"].get("worm_export_tar", "cdecl")
    worm_export_tar.argtypes = [
        POINTER(WormContext),
        WormExportTarCallback,
        POINTER(None),
    ]
    worm_export_tar.restype = WormError

WormExportTarIncrementalCallback = CFUNCTYPE(
    UNCHECKED(c_int), POINTER(c_ubyte), c_uint, uint32_t, uint32_t, POINTER(None)
)  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 2303

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 2315
if _libs["libWormAPI"].has("worm_export_tar_incremental", "cdecl"):
    worm_export_tar_incremental = _libs["libWormAPI"].get(
        "worm_export_tar_incremental", "cdecl"
    )
    worm_export_tar_incremental.argtypes = [
        POINTER(WormContext),
        POINTER(c_ubyte),
        c_int,
        POINTER(c_ubyte),
        c_int,
        POINTER(worm_uint),
        POINTER(worm_uint),
        WormExportTarIncrementalCallback,
        POINTER(None),
    ]
    worm_export_tar_incremental.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 2454
if _libs["libWormAPI"].has("worm_export_tar_incremental_ex", "cdecl"):
    worm_export_tar_incremental_ex = _libs["libWormAPI"].get(
        "worm_export_tar_incremental_ex", "cdecl"
    )
    worm_export_tar_incremental_ex.argtypes = [
        POINTER(WormContext),
        POINTER(c_ubyte),
        c_int,
        POINTER(c_ubyte),
        c_int,
        worm_uint,
        POINTER(c_int),
        POINTER(worm_uint),
        POINTER(worm_uint),
        WormExportTarIncrementalCallback,
        POINTER(None),
    ]
    worm_export_tar_incremental_ex.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 2482
if _libs["libWormAPI"].has("worm_export_tar_incremental_sizeInSectors", "cdecl"):
    worm_export_tar_incremental_sizeInSectors = _libs["libWormAPI"].get(
        "worm_export_tar_incremental_sizeInSectors", "cdecl"
    )
    worm_export_tar_incremental_sizeInSectors.argtypes = [
        POINTER(WormContext),
        POINTER(c_ubyte),
        c_int,
        POINTER(worm_uint),
    ]
    worm_export_tar_incremental_sizeInSectors.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 2507
if _libs["libWormAPI"].has("worm_export_tar_incremental_size", "cdecl"):
    worm_export_tar_incremental_size = _libs["libWormAPI"].get(
        "worm_export_tar_incremental_size", "cdecl"
    )
    worm_export_tar_incremental_size.argtypes = [
        POINTER(WormContext),
        POINTER(c_ubyte),
        c_int,
        POINTER(uint64_t),
    ]
    worm_export_tar_incremental_size.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 2534
if _libs["libWormAPI"].has("worm_export_tar_filtered_time", "cdecl"):
    worm_export_tar_filtered_time = _libs["libWormAPI"].get(
        "worm_export_tar_filtered_time", "cdecl"
    )
    worm_export_tar_filtered_time.argtypes = [
        POINTER(WormContext),
        worm_uint,
        worm_uint,
        String,
        WormExportTarCallback,
        POINTER(None),
    ]
    worm_export_tar_filtered_time.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 2557
if _libs["libWormAPI"].has("worm_export_tar_filtered_transaction", "cdecl"):
    worm_export_tar_filtered_transaction = _libs["libWormAPI"].get(
        "worm_export_tar_filtered_transaction", "cdecl"
    )
    worm_export_tar_filtered_transaction.argtypes = [
        POINTER(WormContext),
        worm_uint,
        worm_uint,
        String,
        WormExportTarCallback,
        POINTER(None),
    ]
    worm_export_tar_filtered_transaction.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 2574
if _libs["libWormAPI"].has("worm_export_lcm_file", "cdecl"):
    worm_export_lcm_file = _libs["libWormAPI"].get("worm_export_lcm_file", "cdecl")
    worm_export_lcm_file.argtypes = [
        POINTER(WormContext),
        String,
        POINTER(POINTER(c_char)),
    ]
    worm_export_lcm_file.restype = WormError

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 2589
if _libs["libWormAPI"].has("worm_export_deleteStoredData", "cdecl"):
    worm_export_deleteStoredData = _libs["libWormAPI"].get(
        "worm_export_deleteStoredData", "cdecl"
    )
    worm_export_deleteStoredData.argtypes = [POINTER(WormContext)]
    worm_export_deleteStoredData.restype = WormError


# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 2598
class struct_anon_8(Structure):
    pass


struct_anon_8.__slots__ = [
    "amount",
    "serialNumber",
]
struct_anon_8._fields_ = [
    ("amount", c_int),
    ("serialNumber", (c_ubyte * int(32)) * int(16)),
]

WormSerialNumberList = struct_anon_8  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 2598

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 2617
for _lib in _libs.values():
    if not _lib.has("worm_lantse_listConnectedTses", "cdecl"):
        continue
    worm_lantse_listConnectedTses = _lib.get("worm_lantse_listConnectedTses", "cdecl")
    worm_lantse_listConnectedTses.argtypes = [
        POINTER(WormContext),
        c_int,
        POINTER(WormSerialNumberList),
    ]
    worm_lantse_listConnectedTses.restype = WormError
    break

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL_publicTypes.h: 98
try:
    WORM_TSE_FW_UPDATE_MAX_CHUNK_SIZE = 496
except:
    pass

# /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL_publicTypes.h: 101
try:
    WORM_EXPORT_TAR_INCREMENTAL_STATE_SIZE = 16
except:
    pass

WormContext = struct_WormContext  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 309

WormInfo = struct_WormInfo  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 597

WormTransactionResponse = struct_WormTransactionResponse  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 1804

WormEntry = struct_WormEntry  # /tmp/Swissbit_TSE_v5.9.1_LAN_TSE_v2.0.11/sdk-offline/sdk/c/include/WormDLL/WormDLL.h: 2051

# No inserted files

# No prefix-stripping
