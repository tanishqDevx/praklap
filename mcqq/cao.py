import random
def load_questions(filename):
    questions = []
    with open(filename, "r") as file:
        for line in file:
            question, answer = line.split("   ")
            questions.append((question, answer.lower()))
    return questions
def quiz(questions, player_name):
    points = 0
    if(questions == []):
        print("empty file")
        return
    selected_questions = random.sample(questions, 4)
    result_filename = f"{player_name}.txt"
    result_file = open(result_filename, "w")
    for q, correct_answer in selected_questions:
        print(q)
        player_answer = input().lower()
        result_file.write(f"Question: {q}\n")
        result_file.write(f"Your Answer: {player_answer}\n")
        result_file.write(f"Correct Answer: {correct_answer}\n\n")
        if player_answer == correct_answer:
            points += 1
    result_file.write(f"Total Score: {points}/4\n")
    result_file.close()
name = input("Welcome to the quiz!\nEnter your name: ")
print("1 -> Science\n2 -> History\n3 -> Geography\n")
print("Select 1, 2, or 3")
x = int(input())
sci = load_questions("science.txt")
history = load_questions("history.txt")
geography = load_questions("geography.txt")
if x == 1:
    quiz(sci, name)
elif x == 2:
    quiz(history, name)
elif x == 3:
    quiz(geography, name)
else:
    print("Invalid selection.")