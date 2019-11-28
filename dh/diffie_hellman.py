from codecs import getdecoder, getencoder

_hexdecoder = getdecoder("hex")
_hexencoder = getencoder("hex")


def str_xor(a, b):
    return bytes(a_i ^ b_i for a_i, b_i in zip(bytearray(a), bytearray(b)))


def hex_decode(data):
    return _hexdecoder(data)[0]


def hex_encode(data):
    return _hexencoder(data)[0].decode("utf-8")


def bytes_to_long(raw):
    return int(hex_encode(raw), 16)


def long_to_bytes(n):
    res = hex(int(n))[2:]
    s = hex_decode(res)
    return s.rjust(Curve.SIZE, b'\x00')


def mod_invert(a, n):
    """
    # k^-1 = p - (-k)^-1 mod p
    """

    if a < 0:
        return n - mod_invert(-a, n)
    t, new_t = 0, 1
    r, new_r = n, a
    while new_r:
        quotinent = r // new_r
        t, new_t = new_t, t - quotinent * new_t
        r, new_r = new_r, r - quotinent * new_r
    if r > 1:
        return -1
    if t < 0:
        t += n
    return t


class Curve:
    SIZE = 32

    def __init__(self, p, a, b):
        self.p = bytes_to_long(p)
        self.a = bytes_to_long(a)
        self.b = bytes_to_long(b)

    def _pos(self, v):
        if v < 0:
            return v + self.p
        return v

    def _add(self, p1x, p1y, p2x, p2y):
        if p1x == p2x and p1y == p2y:
            t = ((3 * p1x * p1x + self.a) * mod_invert(2 * p1y, self.p)) % self.p
        else:
            tx = self._pos(p2x - p1x) % self.p
            ty = self._pos(p2y - p1y) % self.p
            t = (ty * mod_invert(tx, self.p)) % self.p
        tx = self._pos(t * t - p1x - p2x) % self.p
        ty = self._pos(t * (p1x - tx) - p1y) % self.p
        return tx, ty

    def scalar_multiply(self, degree, point):
        x, y = point
        tx, ty = x, y
        degree -= 1
        if not degree:
            raise ValueError("Degree error")

        while degree:
            if degree & 1:
                tx, ty = self._add(tx, ty, x, y)
            degree = degree >> 1
            x, y = self._add(x, y, x, y)
        return tx, ty


class DiffieHellman:
    def __init__(self):
        pass

    def run(self):
        return True


if __name__ == '__main__':
    dh = DiffieHellman()
    s = dh.run()
