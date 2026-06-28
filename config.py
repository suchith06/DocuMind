"""
config.py
=========
One place for every setting in the project.

Everything that you might want to tweak lives here, so you never have to
hunt through the rest of the code. The values are loaded from your .env
file (for secrets) and from sensible defaults (for everything else).
"""

import os
from dotenv import load_dotenv

# Read the .env file and make its values available via os.getenv(...)
load_dotenv()

# -------------------------------------------------------------------
# 1. IBM watsonx.ai credentials  (loaded from your .env file)
# -------------------------------------------------------------------
WATSONX_APIKEY = os.getenv("WATSONX_APIKEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
WATSONX_URL = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")

# -------------------------------------------------------------------
# 2. Which models to use
# -------------------------------------------------------------------
# The "brain" that writes the answers (a Large Language Model).
# IBM Granite is IBM's own open model and is a great default.
LLM_MODEL_ID = "ibm/granite-3-8b-instruct"

# The model that turns text into numbers ("embeddings") so we can
# search documents by meaning instead of by exact keywords.
EMBEDDING_MODEL_ID = "ibm/slate-30m-english-rtrvr"

# -------------------------------------------------------------------
# 3. How the LLM should behave
# -------------------------------------------------------------------
# Lower temperature  = more focused, factual answers (good for RAG).
# Higher temperature = more creative, varied answers.
LLM_TEMPERATURE = 0.2

# The maximum length of a single answer, measured in "tokens"
# (a token is roughly 3/4 of a word).
LLM_MAX_NEW_TOKENS = 400

# -------------------------------------------------------------------
# 4. How documents are split and searched (the RAG settings)
# -------------------------------------------------------------------
# Big documents are cut into smaller "chunks" before storing.
CHUNK_SIZE = 800        # characters per chunk
CHUNK_OVERLAP = 150     # characters shared between neighbouring chunks
                        # (overlap keeps sentences from being cut in half)

# How many of the most relevant chunks to feed to the LLM per question.
TOP_K = 4

# -------------------------------------------------------------------
# 5. File locations
# -------------------------------------------------------------------
# Folder that holds the documents you want to ask questions about.
DOCUMENTS_DIR = os.path.join(os.path.dirname(__file__), "documents")

# Folder where the vector database is saved on disk, so you don't have
# to re-process your documents every time you restart the app.
VECTOR_DB_DIR = os.path.join(os.path.dirname(__file__), "vector_store")


def check_credentials():
    """
    Make sure the user has filled in their .env file.
    Returns a helpful message if something is missing, otherwise None.
    """
    missing = []
    if not WATSONX_APIKEY or WATSONX_APIKEY.startswith("your-"):
        missing.append("WATSONX_APIKEY")
    if not WATSONX_PROJECT_ID or WATSONX_PROJECT_ID.startswith("your-"):
        missing.append("WATSONX_PROJECT_ID")

    if missing:
        return (
            "Missing credentials: " + ", ".join(missing) + ".\n"
            "Open the .env file and paste in your real IBM watsonx.ai values. "
            "See .env.example for instructions."
        )
    return None
