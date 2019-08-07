conns = {}


def get_conn(name):
    return conns.get(name)


def set_conn(name, c):
    conns[name] = c
    return c
