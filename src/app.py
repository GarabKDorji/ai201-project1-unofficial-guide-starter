"""The Unofficial Guide — end-to-end app (Milestone 5 interface).

Ties the whole pipeline together behind one ask() function and a small Gradio
UI: a question goes in, the retriever finds the most relevant student reviews /
Reddit comments, and the generator writes a grounded answer that cites its own
sources inline (RuleBot style) — so the citation is always consistent with what
the model actually answered, and a refusal naturally carries no sources.

Run from the src/ folder:

    python app.py
"""

import gradio as gr

from retriever import embed_and_store, retrieve
from generator import answer_from_chunks


def ask(question: str) -> str:
    """End-to-end: retrieve context and return a grounded, self-cited answer."""
    question = (question or "").strip()
    if not question:
        return "Please enter a question."

    chunks = retrieve(question)
    if not chunks:
        return "I don't have any documents to answer from yet."

    # The LLM writes the answer AND its [Source: ...] citations in one go, so
    # the sources always match what it actually used (and a refusal has none).
    return answer_from_chunks(question, chunks)


# ---------------------------------------------------------------------------
# Gradio UI
# ---------------------------------------------------------------------------
def handle_query(question):
    return ask(question)


with gr.Blocks(title="The Unofficial Guide") as demo:
    gr.Markdown(
        "# 🎓 The Unofficial Guide\n"
        "Ask about UTEP CS professors and courses — answers come only from "
        "student reviews and Reddit comments, with sources cited."
    )
    inp = gr.Textbox(
        label="Your question",
        placeholder="e.g. What do students say about Daniel Mejia's teaching style?",
    )
    btn = gr.Button("Ask", variant="primary")
    answer = gr.Textbox(label="Answer", lines=10)
    btn.click(handle_query, inputs=inp, outputs=answer)
    inp.submit(handle_query, inputs=inp, outputs=answer)


if __name__ == "__main__":
    # Make sure the vector store is built before serving (no-op if it exists).
    embed_and_store()
    demo.launch()
