from task2_chunks import make_chunks
from lab6_search import Retriever

docs = {
    "it": "A forgotten password can be reset using the recovery link.",
    "assessment": "Assignments are uploaded through the learning portal."
}
records = make_chunks(docs, "sentence")
for backend in ["tfidf", "embedding"]:
    engine = Retriever(records, backend)
    print("Backend:", backend)
    for record, score in engine.search("How can I regain access to my account?", k=2):
        print(record["id"], round(score, 3), record["text"])
