from random import randrange
from math import gcd, sqrt


def testTrialDiv(p: int, threshold=0) -> bool:
    for i, d in enumerate(range(2, int(sqrt(p)))):
        if p % d == 0:
            return False
        
        if threshold and i == threshold:
            return False
        
    return True


def testMillerRabin(p: int, k: int) -> bool:
    s, d = 0, p - 1
    while d % 2 == 0:
        d //= 2; s += 1

    for _ in range(k):
        isStrongPseudoprime = False
        x = randrange(2, p, 1)

        if gcd(x, p) > 1:
            return False
        
        if (xd := pow(x, d, p)) == 1 or xd == p - 1:
            continue
        else:
            for _ in range(1, s):
                if (xd := pow(xd, 2, p)) == p - 1:
                    isStrongPseudoprime = True
                    break
                elif xd == 1:
                    return False
            
            if isStrongPseudoprime == False:
                return False
            
    return True

