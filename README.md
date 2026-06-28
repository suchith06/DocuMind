# DocuMind — a RAG-powered Document Q&A Assistant

DocuMind lets you **ask questions about your own documents** and get answers
written in plain language, with the source files cited. Drop some PDFs or text
files into a folder, run one command, and chat with them in your browser.

It is a capstone project that combines the two IBM courses:

| Course | What it taught | Where it shows up here |
|---|---|---|
| **Develop Generative AI Applications: Get Started** | Connecting to an LLM, prompt engineering, building a web app | `src/llm.py`, the prompt template in `src/rag_pipeline.py`, and the Gradio UI in `src/app.py` |
| **Build RAG Applications: Get Started** | Loading, chunking, embedding, retrieving, and grounding answers | The full pipeline in `src/rag_pipeline.py` |

Everything runs on **IBM watsonx.ai** (the Granite LLM + the Slate embedding model).

---

## 1. The big idea in one minute

A normal LLM answers from memory, so it can "hallucinate" and it knows nothing
about *your* private files. **RAG (Retrieval-Augmented Generation)** fixes both
problems by adding a search step before the model answers:

1. Find the parts of your documents that relate to the question. *(Retrieve)*
2. Paste those parts into the prompt as context. *(Augment)*
3. Let the LLM answer using only that context. *(Generate)*

The result: answers grounded in your documents, with sources you can check.

---

## 2. How it works (architecture)

There are two phases. The first runs once to prepare your documents; the second
runs every time you ask a question.

```
PHASE A — Indexing (happens once, or whenever your documents change)

   documents/*.txt,*.pdf
            │
            ▼
   ┌──────────────┐   ┌──────────────┐   ┌───────────────────┐   ┌──────────────┐
   │  1. LOAD     │──▶│  2. SPLIT    │──▶│ 3. EMBED          │──▶│  STORE in    │
   │  read files  │   │  into chunks │   │ (watsonx Slate)   │   │  Chroma DB   │
   └──────────────┘   └──────────────┘   └───────────────────┘   └──────────────┘
                                                                  vector_store/


PHASE B — Answering (happens for every question)

   Your question
        │
        ▼
   ┌───────────────────┐   ┌──────────────────────┐   ┌───────────────────────┐
   │ 4. RETRIEVE       │──▶│ 5. BUILD THE PROMPT   │──▶│ 6. GENERATE answer    │
   │ closest chunks    │   │ context + question    │   │ (watsonx Granite LLM) │
   │ from Chroma DB    │   │ via prompt template   │   │                       │
   └───────────────────┘   └──────────────────────┘   └───────────────────────┘
                                                                  │
                                                                  ▼
                                                      Answer + cited sources
                                                       shown in the web app
```

### Key terms (quick glossary)
- **Chunk** — a small slice of a document (a few hundred characters). Smaller
  slices make search more precise.
- **Embedding** — a list of numbers representing the *meaning* of text. Similar
  meanings get similar numbers, which is how we search by meaning, not keywords.
- **Vector store** — a database (here, **Chroma**) that holds embeddings and
  quickly finds the closest ones to your question.
- **top k** — how many of the closest chunks we feed to the model (set to 4 in
  `config.py`).
- **Temperature** — how creative the model is; we keep it low (0.2) for factual,
  grounded answers.

---

## 3. Project layout

```
documind/
├── README.md            ← you are here
├── requirements.txt     ← the libraries to install
├── .env.example         ← template for your secret keys
├── .gitignore
├── config.py            ← every setting in one place (models, chunk size, etc.)
├── documents/           ← put YOUR files here (two samples included)
│   ├── generative_ai_basics.txt
│   └── rag_explained.txt
├── vector_store/        ← created automatically on first run
└── src/
    ├── llm.py           ← connects to watsonx LLM + embeddings  (GenAI course)
    ├── rag_pipeline.py  ← load → split → embed → retrieve → generate  (RAG course)
    └── app.py           ← the Gradio web app you run
```

---

## 4. Setup (step by step)

You'll need Python 3.10+ and a free IBM Cloud account.

### Step 1 — Get your IBM watsonx.ai credentials
You need three things:

1. **API key** — go to <https://cloud.ibm.com/iam/apikeys> → **Create** → copy
   the key (you only see it once).
2. **Project ID** — open your project in watsonx.ai
   (<https://dataplatform.cloud.ibm.com/wx/home>), then **Manage → General →
   Project ID**. If you have no project yet, create one and associate a
   *Watson Machine Learning* service instance with it (the free "Lite" plan works).
3. **Service URL** — based on your region, e.g. `https://us-south.ml.cloud.ibm.com`.
   Full list is inside `.env.example`.

### Step 2 — Install the libraries
From inside the `documind/` folder:

```bash
# (recommended) create an isolated environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### Step 3 — Add your keys
Copy the template and fill in your real values:

```bash
# Windows:
copy .env.example .env
# macOS/Linux:
cp .env.example .env
```

Then open `.env` in any editor and paste your API key, Project ID, and URL.
**Never share this file** — it holds your private key.

### Step 4 — Check the connection (optional but recommended)
```bash
python src/llm.py
```
If your keys are correct, the model will reply with a short hello.

---

## 5. Run it

```bash
python src/app.py
```

The first run will read the sample documents, split them, create embeddings, and
build the `vector_store/` (this takes a moment). Then it prints a local link such
as `http://127.0.0.1:7860` — open it in your browser and start asking questions.

### Try these questions
- "What is RAG and why is it useful?"
- "What are the five steps of a RAG pipeline?"
- "What does temperature do?"
- "What is an embedding, in simple terms?"

Watch how each answer ends with the **source file** it came from.

---

## 6. Make it your own

- **Use your own documents:** drop `.pdf` or `.txt` files into `documents/`,
  delete the `vector_store/` folder, and restart. It will rebuild automatically.
- **Tune behaviour:** edit `config.py` — try a larger `TOP_K` for broader answers,
  a smaller `CHUNK_SIZE` for finer search, or a higher `LLM_TEMPERATURE` for more
  creative replies.
- **Swap the model:** change `LLM_MODEL_ID` in `config.py` to any model your
  watsonx project supports.

---

## 7. Troubleshooting

| Symptom | Likely cause / fix |
|---|---|
| `Missing credentials...` message | Your `.env` is missing or still has the placeholder values. Re-check Step 3. |
| `403` / authentication errors | API key, Project ID, or URL is wrong, or your project has no Watson Machine Learning service attached. |
| Answers say *"I couldn't find that in the documents"* | The info isn't in your files, or the `vector_store/` is stale. Delete `vector_store/` and restart to rebuild. |
| Changed the documents but answers didn't change | The old index is cached. Delete the `vector_store/` folder and restart. |
| `ModuleNotFoundError` | The virtual environment isn't active, or `pip install -r requirements.txt` didn't finish. |
| Port 7860 already in use | Another app is running. Stop it, or change the launch line in `src/app.py`. |

---

## 8. What to say about this project (for your portfolio)

> "I built DocuMind, a Retrieval-Augmented Generation app on IBM watsonx.ai. It
> ingests documents, splits them into chunks, embeds them with IBM's Slate model
> into a Chroma vector store, retrieves the most relevant passages for a user's
> question, and uses the Granite LLM with a constrained prompt to generate
> grounded, source-cited answers — served through a Gradio web interface."

That single sentence covers both courses: generative AI application development
**and** RAG.
