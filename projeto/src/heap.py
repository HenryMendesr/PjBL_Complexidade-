import ctypes
from array import array
from functools import partial
from pathlib import Path

_library = None


def prepare_heap(a):
    global _library
    if not isinstance(a,array) or a.typecode!='H' or a.itemsize!=2:
        raise TypeError("A entrada deve ser array('H') com elementos de 2 bytes.")
    if _library is None:
        path=Path(__file__).resolve().parents[1]/'build/libheap.so'
        if not path.exists():
            raise RuntimeError('Compile primeiro: python3 projeto/scripts/compilar.py')
        _library=ctypes.CDLL(str(path))
        _library.heap_unique.argtypes=[ctypes.POINTER(ctypes.c_uint16),ctypes.c_size_t]
        _library.heap_unique.restype=ctypes.c_size_t
    view=(ctypes.c_uint16*len(a)).from_buffer(a)
    return partial(_library.heap_unique,view,len(a))


def heap_unique(a):
    return prepare_heap(a)()
