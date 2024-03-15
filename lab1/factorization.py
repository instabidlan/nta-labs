from random import randint
from math import gcd, log10, sqrt
from tests import testMillerRabin, testTrialDiv


class rhoPollard:
    def __init__(self, n: int) -> None:
        self._n = n
        assert type(self._n) == int, "Provided n is not an integer"

        self._f = lambda x: (x**2 + 1) % self._n
        self._orbit = [randint(1, self._n)]

    
    def buildOrbit(self, k: int) -> None:
        for _ in range(k):
            self._orbit.append(self._f(self._orbit[-1]))


    def isPrime(self) -> bool:
        if log10(self._n) <= 65537**2:
            is_prime = testTrialDiv(self._n)
        else:
            is_prime = testMillerRabin(self._n)

        return is_prime


    def variantClassic(self) -> int:
        while True:
            if self.isPrime():
                return self._n

            init_orbit_len = len(self._orbit)
            self.buildOrbit(10)

            for j in range(init_orbit_len, len(self._orbit)):
                for k in range(0, j):
                    d = gcd(abs(self._orbit[j] - self._orbit[k]), self._n)

                    if d != 1 and d != self._n:
                        return d
                    
    
    # def variantFloyd(self) -> int:
    #     while True:
    #         if self.isPrime():
    #             return self._n
            
    #         init_orbit_len = len(self._orbit)
    #         self.buildOrbit(10)

    #         for j in range(init_orbit_len, int(sqrt(len(self._orbit)))):
    #             d = gcd(abs(self._orbit[j ** 2] - self._orbit[j]), self._n)

    #             if d != 1 and d != self._n:
    #                 return d


if __name__ == "__main__":
    n = 1032443261
    A = rhoPollard(n)
    print(A.variantClassic())
    # print(A.variantFloyd())
        