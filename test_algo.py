import multiprocessing

def funSquare(num):
    return num ** 2

if __name__ == '__main__':
    pool = multiprocessing.Pool()
    results = pool.map(funSquare, range(10))
    print(results)