from summary_module import summarize_text

print("Testing EduGenie Summary Module...")

text = """
Artificial Intelligence is a branch of computer science.
It focuses on creating machines that can perform tasks
that normally require human intelligence. AI is used in
speech recognition, image recognition, decision making,
healthcare, education, and many other fields.
"""

summary = summarize_text(text)

print("\nSummary:")
print(summary)
