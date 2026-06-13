"""Grounded answer generation for The Unofficial Guide (Milestone 5).

Pipeline tail end: take a user question, retrieve the most relevant chunks
(retriever.py), and ask the Groq LLM to answer USING ONLY those chunks.

Grounding is enforced two ways:
  1. We only ever put the retrieved chunks in the prompt — the model is given
     nothing else to draw from.
  2. The system prompt explicitly forbids outside/training knowledge and tells
     the model to say it doesn't know when the chunks don't cover the question.

Run directly to answer the 5 evaluation questions from planning.md:

    python generator.py
"""

from __future__ import annotations

import os

from dotenv import load_dotenv
from groq import Groq

from retriever import retrieve

# ---------------------------------------------------------------------------
# Configuration (model from the Architecture diagram in planning.md)
# ---------------------------------------------------------------------------
load_dotenv()  # reads GROQ_API_KEY from the .env file
LLM_MODEL = "llama-3.3-70b-versatile"

_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# The grounding contract. This is the heart of Milestone 5: it is what stops
# the model from inventing rules or using what it learned in training.
SYSTEM_PROMPT = """You are The Unofficial Guide, an assistant that answers \
questions about UTEP Computer Science professors and courses using ONLY \
student reviews and Reddit comments provided to you.

Rules you must follow:
- Answer using ONLY the information in the "Retrieved context" below. Treat it \
as your entire world of knowledge.
- Do NOT use any outside or prior knowledge, and do NOT add facts, names, \
courses, or opinions that are not present in the context.
- Do NOT guess or fill in gaps. If the context does not contain enough \
information to answer, reply exactly: "I don't have any information regarding \
that." and nothing else (no sources).
- Report what students actually said, staying close to their specific points \
and details rather than condensing everything into a vague summary. Keep a \
neutral, professional tone and do not repeat rude or offensive wording verbatim.
- When you do answer, end with a "Sources:" line listing ONLY the sources you \
actually used, copied from the [Source: ...] labels in the context. Do not \
cite a source you did not use, and do not invent sources."""


def _format_context(chunks: list[dict]) -> str:
    """Turn retrieved chunks into a numbered context block with source labels.

    Each chunk gets a [Source: ...] label built from its metadata so the model
    can cite it. Reviews are labeled by professor; comments by thread title.
    """
    blocks = []
    for i, chunk in enumerate(chunks, start=1):
        m = chunk["metadata"]
        if m.get("unit_kind") == "REVIEW":
            label = f"{m.get('professor', 'Unknown')} — {m.get('source')}"
        else:  # COMMENT
            label = f"{m.get('title', 'Reddit thread')} — {m.get('source')}"
        url = m.get("url", "")
        blocks.append(
            f"--- Chunk {i} ---\n"
            f"[Source: {label} | {url}]\n"
            f"{chunk['text']}"
        )
    return "\n\n".join(blocks)


def answer_from_chunks(query: str, chunks: list[dict]) -> str:
    """Generate a grounded, cited answer from already-retrieved ``chunks``."""
    if not chunks:
        return ("I don't have any documents to answer from. Make sure the "
                "vector store has been built (run retriever.py).")

    context = _format_context(chunks)
    user_message = (
        f"Question: {query}\n\n"
        f"Retrieved context:\n{context}"
    )

    response = _client.chat.completions.create(
        model=LLM_MODEL,
        temperature=0,  # deterministic, less room to drift from the context
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )
    return response.choices[0].message.content


def generate_answer(query: str) -> str:
    """Retrieve context for ``query`` and return a grounded, cited answer."""
    return answer_from_chunks(query, retrieve(query))


# ---------------------------------------------------------------------------
# Manual check: run the 5 evaluation questions from planning.md.
# ---------------------------------------------------------------------------
def _main() -> None:
    questions = [
        "What do student reviews say about Daniel Mejia's teaching style?",
        "What do student reviews say about Kuldeep Singh's course difficulty or workload?",
        "What do student reviews say about Monika Akbar's helpfulness or class experience?",
        "Do students describe the UTEP CS program as worth it? Why or why not?",
        "What advice do students give about succeeding in UTEP CS courses?",
    ]
    for q in questions:
        print("\n" + "=" * 75)
        print("Q:", q)
        print("=" * 75)
        print(generate_answer(q))


if __name__ == "__main__":
    _main()
