import random

def load_questions(filename):
    return [tuple(line.strip().split("   ")) for line in open(filename, "r")]

def quiz(questions):
    points = 0
    selected_questions = random.sample(questions, 4)
    for q, a in selected_questions:
        print(q)
        ans = input().strip().lower()
        if ans == a:
            points += 1
    return points

name = input("Welcome to the quiz!\nEnter your name: ")
print("1 -> Science\n2 -> History\n3 -> Geography\n")
print("Select 1, 2, or 3")
x = int(input())

sci = load_questions("science.txt")
history = load_questions("history.txt")
geography = load_questions("geography.txt")

if x == 1:
    points = quiz(sci)
elif x == 2:
    points = quiz(history)
elif x == 3:
    points = quiz(geography)
else:
    print("Invalid selection.")
    exit()

print(f"Your score: {points}/4")
