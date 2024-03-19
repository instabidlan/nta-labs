from random import randint
from math import gcd, sqrt, exp, log
from tests import isPrime


class rhoPollard:
    def __init__(self, n: int) -> None:
        self._n = n
        assert type(self._n) == int, "Provided n is not an integer"

        self._f = lambda x: (x**2 + 1) % self._n
        self._orbit = [randint(1, self._n)]

    
    def buildOrbit(self, k: int) -> None:
        for _ in range(k):
            self._orbit.append(self._f(self._orbit[-1]))


    def variantClassic(self) -> int:
        while True:
            if isPrime(self._n):
                return -1

            init_orbit_len = len(self._orbit)
            self.buildOrbit(10)

            for j in range(init_orbit_len, len(self._orbit)):
                for k in range(0, j):
                    d = gcd(abs(self._orbit[j] - self._orbit[k]), self._n)

                    if d != 1 and d != self._n:
                        self._n //= d
                        return d
                    
    
    def variantFloyd(self) -> int:
        while True:
            if isPrime(self._n):
                return -1
            
            init_orbit_len = int(sqrt(len(self._orbit)))
            self.buildOrbit(16)

            for j in range(init_orbit_len, int(sqrt(len(self._orbit)))):
                d = gcd(abs(self._orbit[j ** 2] - self._orbit[j]), self._n)

                if d != 1 and d != self._n:
                    self._n //= d
                    return d
                

class Factorization:
    def __init__(self, n: int) -> None:
        self._n = n
        self._factors = []


    def factorizePollard(self) -> None:
        r = rhoPollard(self._n)
        while True:
            d = r.variantFloyd()
            if d == -1:
                break

            self._factors.append(d)

        return self._factors + [r._n]


class BrillhartMorrison:
    def __init__(self, n: int) -> None:
        self._n = n
        assert type(self._n) == int, "Provided n is not an integer"

        self._D = self._n
        self._sqrtD = sqrt(self._D)
        self._alpha = sqrt(self._D)
        self._a = int(self._alpha)
        self._v = 1
        self._u = self._a * self._v
        self._b = self._a
        self.B = []
        self.Bsmooth = []
        self.aa = [self._a]
        self.bb = [1, self._b]
        self.b2 = [1, pow(self.bb[1], 2, self._n)]
        self.Vectors = []


    def symLegendre(self, a: int, p: int) -> int:
        l = pow(a, ((p - 1) // 2), p)
        return l if l != p - 1 else -1
    

    def buildB(self) -> None:
        L = exp(sqrt(log(self._n) * log(log(self._n))))
        maxP = int(pow(L, (1 / sqrt(2))))
        sieve = [True] * maxP
        for i in range(2, int(sqrt(maxP))):
            for j in range(i*i, maxP, i):
                sieve[j] = False

        initB = [i for i in range(1, maxP) if sieve[i]]

        for p in initB:
            if self.symLegendre(n, p) == 1:
                self.B.append(p)

        print(self.B)


    def cfrac(self) -> None:
        # BUG: if n = x^2, there is a ZeroDivisionError
        # BUG: if n = 123211, algo stucks here
        self._v = (self._D - self._u**2) / self._v
        self._alpha = (self._sqrtD + self._u) / self._v
        self._a = int(self._alpha)
        self._u = self._a * self._v - self._u

        i = len(self.bb) - 1
        self.aa.append(self._a)
        self.bb.append((self.aa[i] * self.bb[i] + self.bb[i - 1]) % self._n)
        self.b2.append(pow(self.bb[-1], 2, self._n))


    def foo(self) -> None:
        self.buildB()
        while len(self.Bsmooth) != len(self.B) + 1:
            self.cfrac()
            b = self.b2[-1]
            temp_v = [0] * (len(self.B) + 1)
            for i, d in enumerate(self.B):
                if d > sqrt(self.b2[-1]) + 1:
                    break

                if b % d == 0:
                    b //= d
                    temp_v[i] += 1

                    if b == 1:
                        self.Bsmooth.append(self.b2[-1])
                        self.Vectors.append({self.b2[-1]: temp_v})

        print(self.Bsmooth)
        print(self.Vectors)
                    
    # def fastGauss(self) -> None:

                    
    



if __name__ == "__main__":
    n = 1232113
    # n = 1032
    # n = 54339119
    # A = rhoPollard(n)
    # A = Factorization(n)
    # f = A.factorizePollard()
    # l = Legendre(124431, 9921311)
    # print(A.variantClassic())
    # print(A.variantFloyd())
    # print(legendre(124431, 9921311))
    b = BrillhartMorrison(n)
    b.foo()
        