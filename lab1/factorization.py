from random import randint, getrandbits
# from numpy import linalg, array, mod
import numpy as np
from math import gcd, sqrt, exp, log
from tests import isPrime
import galois

from time import sleep


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
            init_orbit_len = len(self._orbit)
            self.buildOrbit(10)

            for j in range(init_orbit_len, len(self._orbit)):
                for k in range(0, j):
                    d = gcd(abs(self._orbit[j] - self._orbit[k]), self._n)

                    if d != 1 and d != self._n:
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
                    return d
                

# class Factorization:
#     def __init__(self, n: int) -> None:
#         self._n = n
#         self._factors = []


#     def factorizePollard(self) -> None:
#         r = rhoPollard(self._n)
#         while True:
#             d = r.variantFloyd()
#             if d == -1:
#                 break

#             self._factors.append(d)

#         return self._factors + [r._n]


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
        self.B = []
        self.Bsmooth = []
        self.aa = [self._a]
        self.bb = [1, self._a]
        self.b2 = [1, pow(self.bb[1], 2, self._n)]
        self.Vectors = []


    def symLegendre(self, a: int, p: int) -> int:
        l = pow(a, ((p - 1) // 2), p)
        return l if l != p - 1 else -1
    

    def returnPrimesUpToN(self, n: int) -> list:
        sieve = [True] * n
        for i in range(2, int(sqrt(n))):
            for j in range(i*i, n, i):
                sieve[j] = False

        return [i for i in range(1, n) if sieve[i]]
    

    def addNextPrime(self) -> None:
        for p in range(self.B[-1], int(self.B[-1] + self.B[-1]/(25 * ((log(self.B[-1])) ** 2))) + 1):
            if isPrime(p):
                self.B.append(p)
    

    def buildB(self) -> None:
        self.B = []
        L = exp(sqrt(log(self._n) * log(log(self._n))))
        maxP = int(pow(L, 1 / sqrt(2)))

        initB = self.returnPrimesUpToN(maxP)
        for p in initB:
            if self.symLegendre(n, p) == 1:
                self.B.append(p)


    def cfrac(self) -> None:
        # BUG: if n = x^2, there is a ZeroDivisionError
        # BUG: if n = 123211, algo stucks here
        self._v = (self._D - (self._u ** 2)) / self._v
        self._alpha = (self._sqrtD + self._u) / self._v
        self._a = int(self._alpha)
        self._u = self._a * self._v - self._u

        self.aa.append(self._a)
        self.bb.append((self.aa[-1] * self.bb[-1] + self.bb[-2]) % self._n)
        self.b2.append(pow(self.bb[-1], 2, self._n))


    def factorByBase(self, num: int) -> list:
        temp_v = [0] * (len(self.B) + 1)
        for i, d in enumerate(self.B):
            while num > 1:
                if num % d == 0:
                    num //= d
                    temp_v[i] ^= 1
                else:
                    break
        
        if num != 1:
            return None
                
        return temp_v


    def findSmoothB(self) -> None:
        self.buildB()
        print(self.B)
        
        while len(self.Bsmooth) < len(self.B) + 1:
            if self.b2[-1] == 1:
                continue

            vec = self.factorByBase(self.b2[-1])

            if vec:
                self.Bsmooth.append(self.b2[-1])
                self.Vectors.append(vec)
            
            self.cfrac()


    @staticmethod
    def addCols(matrix: list[list], col_ind1: int, col_indicies: list) -> None:
        for j in col_indicies:
            for i in range(len(matrix)):
                matrix[i][col_ind1] ^= matrix[i][j]


    def GEoverGF2(self) -> None:
        for j in range(len(self.Vectors)):
            for i in range(len(self.Vectors)):
                if self.Vectors[i][j] == 1:
                    cols_to_add = []
                    for k in range(len(self.Vectors)):
                        if self.Vectors[i][k] == 1 and k != j:
                            cols_to_add.append(k)
                    
                    self.addCols(self.Vectors, j, cols_to_add)
                    break
                    
                    

        print(str(self.Vectors).replace('], ', ']\n').replace('[[', '[').replace(']]', ']'))
                    


    # def solveSLE(self) -> None:
    #     self.GEoverGF2()
    #     GF = galois.GF(2)

    #     A = GF(self.Vectors)
    #     B = GF([0] * len(self.Vectors))

    #     A_inv = np.linalg.inv(A)
    #     print(A_inv)
        # x = np.mod(np.dot(A_inv, B), 2)
        # print(x)



    # def mainBM(self):
    #     eps = 0
    #     while True:
    #         self.findSmoothB(eps)
    #         try:
    #             self.solveSLE()
    #             break
    #         except:
    #             print(f"Error (eps: {eps})")
    #             eps += 0.005


if __name__ == "__main__":
    # n = 1232113 * 4
    # n = 901667173167834173
    # n = 123211
    # n = 3009182572376191
    n = 3009182572

    # n = 123211
    # n = 54339119

    # A = rhoPollard(n)
    # f = A.variantClassic()
    # print(f)

    b = BrillhartMorrison(n)

    b.findSmoothB()
    b.GEoverGF2()

        