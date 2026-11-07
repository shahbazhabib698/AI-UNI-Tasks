"""Conservative command-line FAQ retrieval chatbot."""
from lab6_search import Retriever

FAQ = [
    {"id": "faq:password", "question": "How do I reset my password?",
     "answer": "Use the recovery link on the login page.", "source": "it_help.txt"},
    {"id": "faq:submit", "question": "Where do I submit my assignment?",
     "answer": "Use the assignment upload page in the learning portal.",
     "source": "assessment.txt"},
    {"id": "faq:late", "question": "Can illness justify a late submission?",
     "answer": "Request an extension with medical evidence before the deadline.",
     "source": "handbook.txt"},
    {"id": "faq:wifi", "question": "How can I connect to campus Wi-Fi?",
     "answer": "Select the campus network and sign in with your university account.",
     "source": "network_guide.txt"},
    {"id": "faq:library", "question": "When does the library close?",
     "answer": "Check the current library notice for today's closing time.",
     "source": "library_notice.txt"}
]

def build_bot(backend="tfidf"):
    records = [dict(row, text=row["question"] + " " + row["answer"]) for row in FAQ]
    return Retriever(records, backend)

def reply(engine, query):
    if not query.strip():
        return "Please enter a question."
    for row in FAQ:
        if query.strip().casefold() == row["question"].casefold():
            return row["answer"] + " [source: " + row["source"] + "]"
    hits = engine.search(query)
    if not hits:
        return "No matching FAQ. Please contact the help desk."
    lines = ["Possible matches; choose or rephrase your question:"]
    for record, score in hits:
        lines.append(record["question"] + f" (similarity {score:.3f})")
    return "\n".join(lines)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", choices=["tfidf", "embedding"], default="tfidf")
    args = parser.parse_args()
    engine = build_bot(args.backend)
    print("FAQ assistant. Type exit to stop.")
    while True:
        try:
            query = input("You: ")
        except (EOFError, KeyboardInterrupt):
            break
        if query.strip().lower() == "exit":
            break
        print("Bot:", reply(engine, query))
