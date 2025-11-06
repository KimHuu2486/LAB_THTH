def ex1_1(n):
    if (n <= 1): 
        return 1
    if (n == 2): 
        return  3
    return ex1_1(n - 1) + 2 * ex1_1(n - 2)

def ex1_2(n):
    if (n <= 1):
        return 3
    if (n == 2):
        return 8
    return 2 * ex1_2(n - 1) + 2 * ex1_2(n - 2)



if __name__ == "__main__":
    print(ex1_1(5))
    print(ex1_2(5))