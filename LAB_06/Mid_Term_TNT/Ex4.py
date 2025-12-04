
def count_step(n):
    steps = [0] * (n + 1)
    steps[0] = 1  # There's one way to stay at the ground (do nothing)
    for i in range(1, n + 1):
        steps[i] += steps[i - 1]  # Step from i-1 to i
        if i >= 2:
            steps[i] += steps[i - 2]  # Step from i-2 to i
        if i >= 5:
            steps[i] += steps[i - 5]  # Step from i-5 to i
    return steps[n]

if __name__ == "__main__":
    n = int(input("Enter the number of steps: "))
    result = count_step(n)
    print(f"The number of ways to climb {n} steps is: {result}")