"""Task 2: source-traceable fixed-window and sentence-aware chunking."""
import re

def word_spans(text):
    return [(match.start(), match.end()) for match in re.finditer(r"\S+", text)]

def windows(text, size=40, overlap=10, offset=0):
    if size <= 0 or not 0 <= overlap < size:
        raise ValueError("Require size > 0 and 0 <= overlap < size")
    spans = word_spans(text)
    result = []
    step = size - overlap
    for i in range(0, len(spans), step):
        j = min(i + size, len(spans))
        result.append((offset + spans[i][0], offset + spans[j - 1][1]))
        if j == len(spans):
            break
    return result

def sentence_chunks(text, size=40):
    if size <= 0:
        raise ValueError("size must be positive")
    # Deliberately simple teaching splitter: punctuation followed by whitespace.
    cuts = [0] + [match.end() for match in re.finditer(r"[.!?]\s+", text)] + [len(text)]
    output, pending, count = [], None, 0
    for start, end in zip(cuts, cuts[1:]):
        segment = text[start:end]
        number = len(segment.split())
        if not number:
            continue
        if number > size:
            if pending is not None:
                output.append(pending)
            output.extend(windows(segment, size=size, overlap=0, offset=start))
            pending, count = None, 0
        elif pending is not None and count + number <= size:
            pending, count = (pending[0], end), count + number
        else:
            if pending is not None:
                output.append(pending)
            pending, count = (start, end), number
    if pending is not None:
        output.append(pending)
    return output

def make_chunks(docs, strategy):
    result = []
    for doc_id, text in docs.items():
        if strategy == "sentence":
            spans = sentence_chunks(text, 40)
        elif strategy in {"0", "10"}:
            spans = windows(text, 40, int(strategy))
        else:
            raise ValueError("Strategy must be '0', '10', or 'sentence'")
        for index, (start, end) in enumerate(spans):
            result.append({
                "id": f"{doc_id}:{index}", "doc": doc_id,
                "source": f"{doc_id}.txt", "start": start, "end": end,
                "text": text[start:end]
            })
    return result

if __name__ == "__main__":
    assert windows("") == []
    assert windows("short text") == [(0, 10)]
    try:
        windows("a b", 2, 2)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid overlap was accepted")
    long_sentence = " ".join(["word"] * 95) + "."
    assert all(len(long_sentence[a:b].split()) <= 40
               for a, b in sentence_chunks(long_sentence))
    sample_docs = {"example": "Reset your password. Keep recovery codes private."}
    for strategy in ["0", "10", "sentence"]:
        for chunk in make_chunks(sample_docs, strategy):
            assert chunk["text"] == sample_docs[chunk["doc"]][chunk["start"]:chunk["end"]]
            print(strategy, chunk)
    print("Task 2 boundary tests passed.")
