import argparse
from array import array
from bitmap import bitmap_unique
from heap import heap_unique
from time import perf_counter


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('algoritmo', choices=['heap', 'bitmap'])
    parser.add_argument('valores', type=int, nargs='*')
    args = parser.parse_args()
    if any(x < 0 or x > 65535 for x in args.valores):
        parser.error('Os valores devem estar entre 0 e 65535.')
    a = array('H', args.valores)
    start = perf_counter()
    u = {'heap': heap_unique, 'bitmap': bitmap_unique}[args.algoritmo](a)
    elapsed = perf_counter() - start
    print('Únicos:', list(a[:u]))
    print('Quantidade:', u)
    print(f'Tempo local: {elapsed:.9f} s')


if __name__ == '__main__':
    main()
