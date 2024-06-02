import timeit

def func1():
    a = 0
    a += 1

def func2():
    a = 0
    a = 1 + a

print(timeit.timeit(func1))
print(timeit.timeit(func2))

