

class C:
    a = []


if __name__ == '__main__':
    b = C.a
    b.append('a')
    print(C.a)