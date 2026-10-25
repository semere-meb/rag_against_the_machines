*This project has been created as part of the 42 curriculum by semebrah.*


# RAG against the machines

## Description
This project is a RAG(Retrieval-Augmented Generation) system, that answers questions about a codebase (vLLM v0.10.1) with the help of a local model (Qwen/Qwen3-0.6B).

In an overview, it does this by going through 4 subsystems:
- Indexing - Reading and organizing the corpus sources in a structured way (`src/indexer.py`: walks `data/raw/vllm-0.10.1/`, filters excluded directories like `.venv`/`__pycache__`, and reads `.py` and `.md` files into structured Pydantic `File` models).
- Retrieval - Collecting the sources that are the most relevant for the asked question. 
- Augmentation - Appending the retrieved sources to a system prompt.
- Generation - Sending the constructed prompt+sources to an LLM and getting the answer back.
