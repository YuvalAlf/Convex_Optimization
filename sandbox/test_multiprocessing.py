import multiprocessing

from symbolic_poly.monom import Monom


def print_hash(num):
    print(hash(Monom({'x': 1})))


def main():
    with multiprocessing.Pool(4) as pool:
        pool.map_async(print_hash, [1,2,3,4,5,6,7])
        pool.close()
        pool.join()


if __name__ == '__main__':
    main()
