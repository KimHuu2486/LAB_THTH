#####
from itertools import product

def binarySeq():
    lists = [''.join(q) for q in product('01', repeat = 8)]
    ans = 0
    for s in lists:
        if s.count('0') == 3:
            ans+=1
    return len(lists), ans

#####
def countSeq():
    lists = [''.join(q) for q in product('abcd', repeat = 5)]
    ans1 = ans2 = 0
    for s in lists:
        if 'a' in s:
            ans2+=1
        if s.count('a') == 1:
            ans1+=1
    return len(lists), ans1, ans2

#####
from itertools import combinations, permutations
def countSeats():
    count = 0
    for seat in combinations(range(6), 4):
        for order in permutations(range(4)):
            count+=1
    return count

if __name__ == "__main__":
    print("Exercise 1: ", binarySeq())

    print("Exercise 2: ", countSeq())

    print("Exercise 3: ", countSeats())