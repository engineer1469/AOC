import dis

def test():
    a = [1, 2]
    a[0], a[1] = a[1], a[0]

dis.dis(test)