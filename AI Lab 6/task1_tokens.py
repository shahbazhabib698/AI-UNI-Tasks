import re

# Some examples for checking tokens
samples = [
    "AI, search!",
    "I can't log in.",
    "help@example.com",
    "CS4944 version 2.1",
    "",
    "یہ ایک مثال ہے"
]

for text in samples:
    # split() separates text wherever there is a space
    space_tokens = text.split()

    # This pattern finds word-like parts
    word_tokens = re.findall(r"\b\w+\b", text, flags=re.UNICODE)

    print("\nText:", repr(text))
    print("Space tokens:", space_tokens)
    print("Number of space tokens:", len(space_tokens))
    print("Word-like tokens:", word_tokens)
    print("Number of word-like tokens:", len(word_tokens))

# Optional: compare with the tokenizer used by the sentence model
try:
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")
    print("\nModel tokens:")
    for text in samples[:2]:
        print(text, "=>", model.tokenizer.tokenize(text))
except Exception as error:
    print("Model tokenizer was not loaded:", error)
    print("The normal tokenization part above has still run.")

print("\nObservation:")
print("1. split() keeps commas and full stops attached to words.")
print("2. The regex separates punctuation and also splits can't into two parts.")
print("3. Removing punctuation or changing capital letters can damage emails and IDs such as CS4944.")
print("This regex is only a simple word-like method. It is not a complete Urdu tokenizer.")
