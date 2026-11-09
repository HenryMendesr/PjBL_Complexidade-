import argparse
from array import array
from bitmap import bitmap_unique
from heap import prepare_heap
from functools import partial
from time import perf_counter


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('algoritmo', choices=['heap', 'bitmap'])
    parser.add_argument('valores', type=int, nargs='*')
    args = parser.parse_args()
    if any(x < 0 or x > 65535 for x in args.valores):
        parser.error('Os valores devem estar entre 0 e 65535.')
    a = array('H', args.valores)
    run = prepare_heap(a) if args.algoritmo == 'heap' else partial(bitmap_unique,a)
    start = perf_counter()
    u = run()
    elapsed = perf_counter() - start
    print('Únicos:', list(a[:u]))
    print('Quantidade:', u)
    print(f'Tempo local: {elapsed:.9f} s')


if __name__ == '__main__':
    main()
