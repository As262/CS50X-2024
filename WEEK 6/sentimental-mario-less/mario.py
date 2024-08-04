while True:
    try:
        n = int(input("Height: "))
        if (n >= 1) and (n <= 8):
            break
    except:
        print("", end="")

spaces = 1

for i in range(n):
    for spaces in range(n - i - 1):
        print(" ", end="")
    for k in range(i + 1):
        print("#", end = "")

    print()
