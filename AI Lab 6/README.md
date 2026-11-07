# Lab 6 - Student Style Version — NLP Fundamentals: Tokenization, Embeddings & Text Chunking

**Course:** CAI601400 — Artificial Intelligence Lab  
**Lab:** 6 (CLO3 / C3: Apply)  
**Project:** Traceable text-retrieval pipeline using synthetic teaching documents

This repository implements the three tasks in the supplied Lab 6 manual. The policy, support, workplace and troubleshooting examples are synthetic and are not real university or company policies.

## Requirements

- Python 3.10+
- Internet for the first download of `all-MiniLM-L6-v2`
- CPU is sufficient; no GPU or paid API is needed

## Setup (Windows PowerShell)

```powershell
cd lab6_nlp
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, use `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal, then activate again.

## Run all tasks

### Task 1 — tokenization and FAQ chatbot

```powershell
python task1_tokens.py
python task1_chatbot_check.py
python guided_chatbot.py --backend tfidf
python guided_suggestions.py
```

The FAQ bot answers only an exact canonical question. For a paraphrase it shows candidate questions and asks the user to rephrase/confirm. It does not invent answers.

### Task 2 — chunking and semantic suggestions

```powershell
python task2_chunks.py
python task2_semantic_check.py
python guided_embeddings.py
```

`task2_chunks.py` implements 40-word windows with overlap 0 or 10 and sentence-aware packing with a 40-word budget. Every chunk stores a document ID, source name and character start/end offsets. The text must equal the source substring at those offsets.

### Task 3 — evaluation and document evidence chatbot

```powershell
python create_dataset.py
python task3_retrieval.py
python document_chatbot.py
```

`create_dataset.py` validates the included data; it does not overwrite it. Task 3 evaluates six configurations: three chunking strategies (`0`, `10`, `sentence`) crossed with TF-IDF and `all-MiniLM-L6-v2` embeddings. It reports development and held-out test Hit@3/MRR@3, chunk count, model load time, encoding time, search time and token-limit audit. It exports `retrieval_log.csv` and `evaluation_summary.csv`.

The document chatbot uses the sentence-aware embedding configuration as a demonstration. It displays candidates and exact source offsets; a user must choose evidence to inspect. It does not automatically assert an answer.

## Other guided scenario scripts

```powershell
python scenario1_handbook.py
python scenario2_support.py
python scenario3_docs.py
python scenario4_workplace.py
python scenario5_equipment.py
python guided_tokens.py
python guided_limits.py
python guided_metrics.py
```

## Dataset and evaluation design

- `corpus.json`: five synthetic documents, each expanded to at least 150 words.
- `queries.json`: eight answerable queries (four development, four test) and two unanswerable queries.
- Relevance is strict: the top-three chunk must come from the labeled document **and contain the complete labeled evidence string**.
- Hit@3 is the fraction of answerable queries with at least one relevant result in the first three. MRR@3 is the mean reciprocal rank of the first relevant result; misses contribute zero.
- Unanswerable queries are logged separately. A nearest-neighbour system can still return a high-scoring candidate for them; similarity is not proof that evidence exists.
- Do not tune a rejection threshold on the held-out test set. The small synthetic dataset supports only limited conclusions.

## Expected limitations and failure cases

1. **Boundary failure:** a fixed word window can split a rule from its exception. The evidence string then fails the strict relevance test even if part of the rule appears.
2. **Paraphrase failure:** TF-IDF can miss a query with little vocabulary overlap (for example, “regain access” versus “password recovery”).
3. **Abbreviation failure:** the teaching sentence splitter treats punctuation followed by whitespace as a sentence boundary and can split at abbreviations such as `Dr.`.
4. **Conflicting scope:** similar passages can belong to different regions, audiences or versions. Metadata filters help only when the metadata is correct and supplied.
5. **Unanswerable query:** both retrieval methods rank the closest available chunks even when the corpus contains no answer. The chatbot therefore requires human inspection/confirmation.

## Reproducibility and honest reporting

Run the commands on your own machine and retain the generated CSV files. Model download time is measured separately from encoding/search. Runtime varies by CPU, cache state, Python/library versions and machine load. Do not copy example scores from another machine or invent results. The report template `Lab6_Report.docx` describes the method and the evidence that must be inserted after running the experiment.

## GitHub submission checklist

- [ ] Include all `.py` files, `corpus.json`, `queries.json`, `requirements.txt`, `README.md`
- [ ] Include `retrieval_log.csv` and `evaluation_summary.csv` generated by your run
- [ ] Include `Lab6_Report.docx` updated with your actual run outputs
- [ ] Do not upload `.venv/`, model caches, credentials or private data
- [ ] Push the repository and submit its URL and final commit ID through the course channel

## References

- Sentence Transformers semantic search: https://www.sbert.net/examples/sentence_transformer/applications/semantic-search/README.html
- Encoder model card: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
- Code structure and task requirements adapted from the supplied CAI601400 Lab 6 manual. The corpus and query labels in this repository are synthetic.


## Before submission

This version uses straightforward Python code and comments so it is easier to read and explain. Run the programs on your own computer. The embedding part needs `sentence-transformers` and an internet connection for the first model download. Do not write made-up scores in the report: copy the real values from `evaluation_summary.csv` after Task 3 runs.
