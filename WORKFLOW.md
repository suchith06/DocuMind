# How DocuMind Works — Explained Simply

This file explains, in everyday language, what happens inside the project
when you use it. No jargon you can't follow. Read it top to bottom.

---

## The one-sentence version

You give DocuMind some documents, you ask a question, and it finds the right
pages and writes you an answer in plain English — like a study buddy who has
read all your files and only answers from them.

---

## A real-life analogy

Imagine a librarian who has read every book in a library.

When you ask, "What does the handbook say about holidays?", the librarian
doesn't recite the whole library from memory (they might get it wrong). Instead
they:

1. Walk to the right shelf and pull out the few pages that mention holidays.
2. Read just those pages.
3. Answer your question using only what's written there.

DocuMind is that librarian. Your documents are the books. The "shelf" it walks
to is a special search system called a **vector store**.

---

## The two phases

DocuMind works in two phases. The first happens once to get ready. The second
happens every time you ask something.

### Phase 1 — Getting the documents ready (happens once)

Think of this as the librarian reading and organising the books before opening.

```
  Your files (.txt / .pdf)
        |
        v
  [ 1. READ ]   Open every file in the "documents" folder.
        |
        v
  [ 2. CUT ]    Slice each file into small pieces ("chunks"),
        |        because small pieces are easier to search.
        v
  [ 3. TAG ]    Turn each chunk into a list of numbers that
        |        captures its MEANING (this is an "embedding").
        v
  [ 4. STORE ]  Save all those numbered chunks in a searchable
                 database (the "vector store" folder).
```

Why numbers? Because computers compare meaning by comparing numbers. Two chunks
about the same idea get similar numbers, even if they use different words. That's
the trick that lets DocuMind search by *meaning*, not just by matching keywords.

You only do this once. The next time you start the app, the organised shelf is
already there waiting.

### Phase 2 — Answering your question (happens every time)

```
  You type a question
        |
        v
  [ 5. FIND ]      Turn your question into numbers too, then grab the
        |           few chunks whose numbers are closest. These are the
        |           most relevant pieces of your documents.
        v
  [ 6. COMBINE ]   Put those chunks + your question together into a clear
        |           instruction for the AI: "Answer using ONLY this text."
        v
  [ 7. ANSWER ]    The IBM watsonx.ai model reads it and writes the answer.
        |
        v
  You get a plain-English answer, plus the file names it came from.
```

The instruction in step 6 is important: it tells the AI to answer **only** from
the documents and to say "I couldn't find that" if the answer isn't there. That's
what keeps it honest and stops it from making things up.

---

## Which file does what

You don't need to touch most of these, but here's the map:

| File | Its job, in plain words |
|------|-------------------------|
| `documents/` | The folder where you drop the files you want to ask about. |
| `config.py` | The settings dial — model names, how big the chunks are, etc. |
| `src/llm.py` | Connects to IBM's AI (the "writer" and the "number-maker"). |
| `src/rag_pipeline.py` | Does the 7 steps above: read, cut, tag, store, find, combine, answer. |
| `src/app.py` | The chat window you actually open in your browser. |
| `vector_store/` | The organised "shelf" — created automatically. Don't edit by hand. |

---

## What happens, start to finish, when you use it

1. You run `python src/app.py`.
2. The app checks your IBM keys are filled in.
3. If the shelf (`vector_store/`) doesn't exist yet, it builds it from your
   documents (Phase 1). If it already exists, it just opens it.
4. A chat page opens in your browser.
5. You type a question and hit Send.
6. DocuMind finds the relevant chunks, asks watsonx.ai, and shows the answer
   with its sources.
7. Ask as many questions as you like — repeat from step 5.

---

## Two terms worth remembering

- **Embedding** — turning text into numbers that represent its meaning. This is
  how the computer "understands" similarity.
- **RAG (Retrieval-Augmented Generation)** — the whole idea of *finding* the
  right text first and *then* letting the AI write the answer from it. Retrieval
  = finding; Generation = writing. That's the entire project in two words.

---

## If you remember just one thing

DocuMind never answers from memory. It always looks things up in your documents
first, then writes the answer from what it found. That's why its answers stay
accurate and come with sources you can check.
