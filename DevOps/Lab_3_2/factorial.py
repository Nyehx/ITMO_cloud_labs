import sys


def factorial(n):
    if n < 0:
        raise ValueError("Факториал не определен.")
    elif n == 0 or n == 1:
        return 1
    else:
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result


def main():
    if len(sys.argv) != 2:
        return

    try:
        n = int(sys.argv[1])
        result = factorial(n)
        print("Факториал равен " + str(result))
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
