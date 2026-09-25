from quiz_module import generate_quiz

print("Testing EduGenie Quiz Module...")

quiz = generate_quiz("Artificial Intelligence")

print("\nEduGenie Quiz:\n")

for i, question in enumerate(quiz["quiz"], 1):

    print(f"{i}. {question['question']}")

    for option in question["options"]:
        print(f"   - {option}")

    print(f"Answer: {question['answer']}")
    print()
