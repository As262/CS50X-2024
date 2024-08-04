from cs50 import get_string

n = get_string("Text:")

letter = 0
space = 0
sentence = 0

for char in n:
    if char.isalpha():
        letter += 1
    elif char ==" ":
        space += 1
    elif char == "!" or char == "." or char == "?":
        sentence += 1

words = space + 1

L = (letter/words) * 100
S = (sentence/words) * 100

grade = 0.0588 * L - 0.296 * S - 15.8

if grade > 16:
    print("Grade 16+")
elif grade < 1:
    print("Before Grade 1")
else:
    print(f"Grade {round(grade)}")


