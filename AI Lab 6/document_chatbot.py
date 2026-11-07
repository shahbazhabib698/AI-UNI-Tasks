"""Interactive source-traceable evidence browser; it never asserts a generated answer."""
import json
from pathlib import Path
from task2_chunks import make_chunks
from lab6_search import Retriever

def main():
    docs = json.loads(Path("corpus.json").read_text(encoding="utf-8"))
    engine = Retriever(make_chunks(docs, "sentence"), "embedding")
    print("Evidence assistant. Type exit to stop.")
    while True:
        try:
            query = input("Question: ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if query.strip().lower() == "exit":
            break
        if not query.strip():
            print("Please enter a question.")
            continue
        hits = engine.search(query, k=3)
        if not hits:
            print("No candidate evidence; rephrase or contact a human.")
            continue
        print("Candidate evidence; relevance must be checked:")
        for number, (record, score) in enumerate(hits, 1):
            print(number, record["id"], f"{score:.3f}",
                  "characters", record["start"], record["end"])
        chosen = input("Choose 1-3 to inspect; Enter if none apply: ")
        if not chosen.isdigit() or not 1 <= int(chosen) <= len(hits):
            print("No answer selected. Rephrase or contact a human.")
            continue
        record, score = hits[int(chosen) - 1]
        print("Retrieved passage:", record["text"])
        print("Source:", record["source"], "document:", record["doc"],
              "characters", record["start"], record["end"])
        print("This is candidate evidence, not a verified answer.")

if __name__ == "__main__":
    main()
