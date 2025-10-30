#####
def count_odd_unique_digits():
    count = 0
    for num in range(100, 1000):
        digits = str(num)
        if num % 2 == 1 and len(set(digits)) == 3:
            count += 1
    return count


#####
import random

def count_unique_with_f():
    chars = ['a', 'b', 'c', 'd', 'e', 'f']
    seen = set()

    for _ in range(1000):
        s = ''.join(random.sample(chars, 3))
        if 'f' in s:
            if s not in seen:
                seen.add(s)

    return len(seen)

#####
def permutations_recursive(s):
    if (len(s) == 1):
        return [s]
    res = []
    for i, char in enumerate(s):
        for perm in permutations_recursive(s[:i] + s[i+1:]):
            res.append(char + perm)
    return res

from itertools import permutations

def permutations_lib(s):
    return [''.join(p) for p in permutations(s)]

#####
from itertools import product

def binarySeq(n):
    return [''.join(p) for p in product('01', repeat = n)]    

def binaryRecur(n, prefix = ""):
    if n == 0:
        print(prefix, end = ", ")
    else:
        binaryRecur(n -1, prefix + '0')
        binaryRecur(n -1, prefix + '1')

#####
from itertools import combinations

def increasingSeq(n, k):
    return list(combinations(range(1, n + 1), k))

def decreasingSeq(n, k):
    seqs = combinations(range(1, n +1), k)
    return list(sorted(s, reverse = True) for s in seqs)


#####

from math import comb

def countCard():
    ans = 0
    for co in range (0, 4):
        for ro in range (1, 14):
            for chuon in range (1, 14):
                bich = 13 - co - ro - chuon
                if 4 <= bich <= 11:
                    ans +=  comb(13, co) * comb(13, ro) * comb(13, chuon) * comb(13, bich)
    return ans


if __name__ == "__main__":

    print("Exercise 1: %d" % count_odd_unique_digits())

    print("Exercise 2: %d" % count_unique_with_f())

    print("Exercise 3: %d" % len(permutations_recursive("abc")))
    print("Permutations: %s" % permutations_recursive("abc"))
    print("Permutations: %s" % permutations_lib("abc"))

    print("Exercise 4: ")
    print("Combinations: %s" % binarySeq(4))
    print("Combinations:", end = " ")
    binaryRecur(4)

    print("\nExercise 5: ")
    print("Increasing: %s" %increasingSeq(5, 3))
    print("Decreasing: %s" %decreasingSeq(5, 3))

    print("Exercise 6: ", countCard())
