import sys


def factorial(n):
    if n < 0:
        raise ValueError("Факториал не определен для отрицательных чисел.")
    elif n == 0 or n == 1:
        return 1
    else:
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result


def main():
    if len(sys.argv) != 2:
        print("Использование: python factorial.py <целое число>")
        return

    try:
        n = int(sys.argv[1])
        result = factorial(n)
        print(f"Факториал {n} равен {result}")
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
