from solution import Solution


def main():
    print("choose n: ")
    n = input()
    if n.isnumeric() and int(n) <= 2:
        print("Error, n must be bigger than 2")
    elif not n.isnumeric():
        print("Error, n must be a number")
    else:
        solution = Solution(int(n))
        solution.solve()


if __name__ == '__main__':
    main()
