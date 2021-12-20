import cython
from libc.math cimport sqrt

def computar(fim: cython.int, inicio: cython.int=1):

    pos: cython.int64 = inicio
    fator: cython.int64 = 1000*1000

    while pos < fim:
        pos+=1
        sqrt((pos - fator) * (pos - fator))
    print(sqrt((pos - fator) * (pos - fator)))


