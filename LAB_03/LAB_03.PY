#####
import math
def count_gcd_greater_than_one(N, K):
    lists = []
    count = 0
    for n in range (1, N + 1):
        if math.gcd(n, K) > 1:
            count+=1
            lists.append(n)
    return count, lists

#####
#Dn ​= (n−1) × (Dn−1 ​+ Dn−2​), D0 ​= 1, D1 ​= 0
def dearrangement(n):
    if n == 0:
        return 1
    if n == 1:
        return 0
    D = [0] * (n + 1)
    D[0] = 1
    D[1] = 0
    for i in range (2, n + 1):
        D[i] = (i - 1) * (D[i - 1] + D[i - 2])
    return D[n]


#####
def color_table(m, n, k):
    total = 0
    for i in range(k + 1):
        total += (-1)**i * math.comb(k, i) * (k - i)**(m * n)
    return total

#####
from  itertools import combinations

def bounded_compositions(S, L, C):
    total = 0
    for r in range(0, L + 1):
        for subset in combinations(range(L), r):
            new_S = S - sum(C[i] + 1 for i in subset)
            if new_S >= 0:
                total += (-1)**r * math.comb(new_S - 1, L - 1)
    return total

if __name__ == "__main__":
    print("Exercise 1: ", count_gcd_greater_than_one(20, 5))

    print("Exercise 2: ", dearrangement(5))

    print("Exercise 3: ", color_table(2, 2, 3))

    print("Exercise 4: ", bounded_compositions(7, 3, [4, 3, 5]))