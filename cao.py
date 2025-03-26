import random

name = input("welcome to quiz\nenter name\n")
print("1 -> science\n2 -> history\n3 -> geo\n")
print("select 1,2,3")
x = int(input())

file = ".txt"
filename = name + file
f = open(filename, "w")

sci = [
    ("What is the SI unit of force?", "newton"),
    ("What is the unit of power?", "watt"),
    ("Which fundamental force keeps planets in orbit?", "gravity"),
    ("What is the charge of an electron?", "negative"),
    ("What is the SI unit of energy?", "joule"),
    ("What type of lens is used in a magnifying glass?", "convex"),
    ("Which gas is most abundant in the sun?", "hydrogen"),
    ("What is the SI unit of frequency?", "hertz")
]

history = [
    ("Who was the first President of the United States?", "washington"),
    ("What year did World War II end?", "1945"),
    ("Which civilization built the pyramids?", "egyptians"),
    ("Who discovered America in 1492?", "columbus"),
    ("What was the name of the Pilgrims' ship?", "mayflower"),
    ("Which wall divided East and West Berlin?", "berlin"),
    ("Who was the Queen during the Elizabethan Era?", "elizabeth"),
    ("What event started World War I?", "assassination")
]

geography = [
    ("What is the largest continent?", "asia"),
    ("Which is the longest river?", "nile"),
    ("What is the capital of France?", "paris"),
    ("Which ocean is the largest?", "pacific"),
    ("What is the tallest mountain?", "everest"),
    ("Which country has the Great Wall?", "china"),
    ("What is the capital of Japan?", "tokyo"),
    ("What is the smallest country?", "vatican")
]

points = 0

if x == 1:
    questions = sci[:]  # Copy the list
    random.shuffle(questions)  # Shuffle it
    for i in range(4):
        print(questions[i][0])
        ans = input().strip().lower()
        if ans == questions[i][1]:
            points += 1
        f.write(questions[i][0] + "\n")
        f.write("Your Answer was " + ans + "\n")
        f.write("Answer is " + questions[i][1] + "\n\n")
        

if x == 2:
    questions = history[:]
    random.shuffle(questions)
    for i in range(4):
        print(questions[i][0])
        ans = input().strip().lower()
        if ans == questions[i][1]:
            points += 1
        f.write(questions[i][0] + "\n")
        f.write("Your Answer was " + ans + "\n")
        f.write("Answer is " + questions[i][1] + "\n\n")
        

if x == 3:
    questions = geography[:]
    random.shuffle(questions)
    for i in range(4):
        print(questions[i][0])
        ans = input().strip().lower()
        if ans == questions[i][1]:
            points += 1
        f.write(questions[i][0] + "\n")
        f.write("Your Answer was " + ans + "\n")
        f.write("Answer is " + questions[i][1] + "\n\n")

f.write("\n\n\n")
f.write("your points is " + str(points) + "\n")
f.close()
