import ctypes
import os

_lib = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "libcrfpp.so"))

_lib.crfpp_new2.argtypes = [ctypes.c_char_p]
_lib.crfpp_new2.restype = ctypes.c_void_p
_lib.crfpp_destroy.argtypes = [ctypes.c_void_p]
_lib.crfpp_destroy.restype = None
_lib.crfpp_strerror.argtypes = [ctypes.c_void_p]
_lib.crfpp_strerror.restype = ctypes.c_char_p
_lib.crfpp_add.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
_lib.crfpp_add.restype = ctypes.c_bool
_lib.crfpp_clear.argtypes = [ctypes.c_void_p]
_lib.crfpp_clear.restype = ctypes.c_bool
_lib.crfpp_size.argtypes = [ctypes.c_void_p]
_lib.crfpp_size.restype = ctypes.c_size_t
_lib.crfpp_xsize.argtypes = [ctypes.c_void_p]
_lib.crfpp_xsize.restype = ctypes.c_size_t
_lib.crfpp_ysize.argtypes = [ctypes.c_void_p]
_lib.crfpp_ysize.restype = ctypes.c_size_t
_lib.crfpp_parse.argtypes = [ctypes.c_void_p]
_lib.crfpp_parse.restype = ctypes.c_bool
_lib.crfpp_y2.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
_lib.crfpp_y2.restype = ctypes.c_char_p


def _b(s):
    return s.encode("utf-8") if isinstance(s, str) else s


def _s(b):
    return b.decode("utf-8") if b else ""


class Tagger(object):
    def __init__(self, arg):
        self._c = _lib.crfpp_new2(_b(arg))
        if not self._c:
            raise RuntimeError(_s(_lib.crfpp_strerror(None)))

    def __del__(self):
        c = getattr(self, "_c", None)
        if c:
            _lib.crfpp_destroy(c)
            self._c = None

    def add(self, line):
        return _lib.crfpp_add(self._c, _b(line))

    def clear(self):
        return _lib.crfpp_clear(self._c)

    def size(self):
        return _lib.crfpp_size(self._c)

    def xsize(self):
        return _lib.crfpp_xsize(self._c)

    def ysize(self):
        return _lib.crfpp_ysize(self._c)

    def parse(self):
        return _lib.crfpp_parse(self._c)

    def y2(self, i):
        return _s(_lib.crfpp_y2(self._c, i))
