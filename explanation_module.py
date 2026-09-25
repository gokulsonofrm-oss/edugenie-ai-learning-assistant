from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

print("Loading EduGenie Explanation Model...")

MODEL_NAME = "MBZUAI/LaMini-Flan-T5-783M"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)


def explain_topic(topic):

    prompt = f"""
Explain the following topic in simple language for a student:

Topic: {topic}

Give a clear and easy-to-understand explanation.
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True
    )

    outputs = model.generate(
        **inputs,
        max_length=200,
        do_sample=False
    )

    explanation = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return explanation
