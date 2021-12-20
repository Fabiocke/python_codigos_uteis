import math
from datetime import datetime
import computa
import time

# Exemplo de processamento usando cython


def main():
    inicio = datetime.now()
    inicio1=time.time()
    computa.computar(fim=50_000_000)

    tempo = datetime.now()-inicio

    print(f'{tempo.total_seconds():.2f}')
    print(time.time()-inicio1)
if __name__=='__main__':
    main()

