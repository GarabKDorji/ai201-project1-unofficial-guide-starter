"""Document ingestion and chunking for The Unofficial Guide (Milestone 3).

Implements the Chunking Strategy from planning.md:

  - The natural unit of meaning in this corpus is ONE student review (Rate My
    Professors) or ONE Reddit post/comment. Each document is a header block
    followed by units separated by a delimiter line:

        --- REVIEW ---   (Rate My Professors files)
        --- POST ---     (first body of a Reddit thread)
        --- COMMENT ---  (each Reddit reply)

    The regex DELIMITER below matches all three.

  - Each unit becomes its own chunk so we never mix opinions from different
    students or professors in the same chunk.

  - Most units are short and kept whole with 0 overlap. Only units longer than
    CHUNK_SIZE characters are split into ~CHUNK_SIZE windows with OVERLAP chars
    of overlap, on word boundaries, to preserve context across the split.

  - Per-chunk metadata (source, url, title, type, professor, course) is carried
    through so the downstream LLM can cite the correct source.

Run directly to inspect the result:

    python src/chunking.py
"""

from __future__ import annotations
import re
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration — these numbers come straight from the Chunking Strategy
# section of planning.md.
# ---------------------------------------------------------------------------
CHUNK_SIZE = 300   # max characters before a single unit gets split
OVERLAP = 100      # characters of overlap when a long unit is split

# The delimiter that separates the natural units inside every document.
# Captures the unit kind (REVIEW / POST / COMMENT) so we can label the chunk.
DELIMITER = re.compile(r"^---\s*(REVIEW|POST|COMMENT)\s*---\s*$", re.MULTILINE)

# Folder holding the raw .txt documents (sits next to src/).
DOCUMENTS_DIR = Path(__file__).resolve().parent.parent / "documents"


@dataclass
class Chunk:
    """A single retrievable chunk plus the metadata needed to cite it."""

    text: str
    metadata: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Header parsing
# ---------------------------------------------------------------------------
def parse_header(raw: str) -> tuple[dict, str]:
    """Split a document into (header_metadata, body).

    The header is the block of ``Key: value`` lines before the first delimiter.
    Returns the parsed metadata dict and the body text that follows it.
    """
    match = DELIMITER.search(raw)
    header_text = raw[: match.start()] if match else raw
    body = raw[match.start():] if match else ""

    metadata: dict = {}
    for line in header_text.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip().lower()
            value = value.strip()
            if key in {"title", "source", "url", "type", "professor"} and value:
                metadata[key] = value
    return metadata, body


# ---------------------------------------------------------------------------
# Long-unit splitting (only used when a unit exceeds CHUNK_SIZE)
# ---------------------------------------------------------------------------
def split_long_text(text: str, chunk_size: int = CHUNK_SIZE,
                     overlap: int = OVERLAP) -> list[str]:
    """Split text longer than ``chunk_size`` into overlapping windows.

    Splits on word boundaries so we don't cut words in half. Short text
    (<= chunk_size) is returned unchanged as a single-element list.
    """
    text = text.strip()
    if len(text) <= chunk_size:
        return [text]

    words = text.split()
    chunks: list[str] = []
    current = ""
    for word in words:
        # +1 for the space we'd add.
        if current and len(current) + 1 + len(word) > chunk_size:
            chunks.append(current)
            # Start the next window with the tail of the current one (overlap).
            tail = current[-overlap:] if overlap else ""
            # Snap the tail to a word boundary so it reads cleanly.
            if tail and " " in tail:
                tail = tail[tail.index(" ") + 1:]
            current = (tail + " " + word).strip() if tail else word
        else:
            current = (current + " " + word).strip() if current else word
    if current:
        chunks.append(current)
    return chunks


def _extract_field(unit_text: str, field_name: str) -> str | None:
    """Pull a single ``Field: value`` line out of a review/comment body."""
    m = re.search(rf"^{field_name}:\s*(.+)$", unit_text, re.MULTILINE | re.IGNORECASE)
    return m.group(1).strip() if m else None


# ---------------------------------------------------------------------------
# Per-document chunking
# ---------------------------------------------------------------------------
def chunk_document(raw: str, doc_name: str) -> list[Chunk]:
    """Turn one document's raw text into a list of Chunk objects."""
    base_meta, body = parse_header(raw)
    base_meta.setdefault("source", doc_name)

    # Split the body on the delimiter, keeping the matched unit kind.
    parts = DELIMITER.split(body)
    # re.split with one capture group yields: ['', kind, unit, kind, unit, ...]
    chunks: list[Chunk] = []
    for i in range(1, len(parts), 2):
        kind = parts[i].strip()          # REVIEW / POST / COMMENT
        unit_text = parts[i + 1].strip()
        if not unit_text:
            continue

        # A POST is the thread's *question*, not an answer — it carries no
        # knowledge, so indexing it would just waste a retrieval slot on a
        # question-shaped chunk. Skip it. The question itself isn't lost: it is
        # prepended to every COMMENT below as the thread context.
        if kind == "POST":
            continue

        # Carry the structured fields a review exposes into metadata.
        course = _extract_field(unit_text, "Course")
        rating = _extract_field(unit_text, "Rating")
        difficulty = _extract_field(unit_text, "Difficulty")

        # Fix A — put the identifying context INTO the embedded text. The
        # embedding model only sees the text, never the metadata, so without
        # this a review never mentions which professor it's about and a comment
        # never mentions which question it answers.
        if kind == "COMMENT":
            # A comment answers the thread's question — give it that question.
            title = base_meta.get("title", "")
            header = f"[Thread: {title}]" if title else ""
        else:  # REVIEW
            # A review's body has the course but not the professor's name.
            prof = base_meta.get("professor", "")
            header = f"[Professor: {prof}]" if prof else ""

        # Reserve room for the header so the FINAL text (header + piece) still
        # fits inside CHUNK_SIZE — we split the content against the smaller
        # budget, then prepend the header to each piece.
        budget = CHUNK_SIZE - (len(header) + 1) if header else CHUNK_SIZE
        for piece in split_long_text(unit_text, chunk_size=budget):
            meta = dict(base_meta)
            meta["unit_kind"] = kind
            if course:
                meta["course"] = course
            if rating:
                meta["rating"] = rating
            if difficulty:
                meta["difficulty"] = difficulty
            text = f"{header}\n{piece}" if header else piece
            chunks.append(Chunk(text=text, metadata=meta))
    return chunks


def load_and_chunk(documents_dir: Path = DOCUMENTS_DIR) -> list[Chunk]:
    """Load every .txt file in ``documents_dir`` and return all chunks."""
    all_chunks: list[Chunk] = []
    for path in sorted(documents_dir.glob("*.txt")):
        raw = path.read_text(encoding="utf-8")
        all_chunks.extend(chunk_document(raw, doc_name=path.name))
    return all_chunks


# ---------------------------------------------------------------------------
# Manual verification (per the AI Tool Plan: print samples + check splits)
# ---------------------------------------------------------------------------
def _main() -> None:
    chunks = load_and_chunk()
    lengths = [len(c.text) for c in chunks]
    split_units = sum(1 for c in chunks if len(c.text) > CHUNK_SIZE)

    print(f"Documents dir : {DOCUMENTS_DIR}")
    print(f"Total chunks  : {len(chunks)}")
    print(f"Char length   : min={min(lengths)} max={max(lengths)} "
          f"avg={sum(lengths)//len(lengths)}")
    print(f"Over {CHUNK_SIZE} chars: {split_units} (should be 0 after splitting)\n")

    print("Per-source chunk counts:")
    counts: dict[str, int] = {}
    for c in chunks:
        counts[c.metadata.get("source", "?")] = counts.get(
            c.metadata.get("source", "?"), 0) + 1
    for src, n in sorted(counts.items()):
        print(f"  {n:>2}  {src}")

    print("\n--- Sample chunks ---")
    for c in chunks[:3]:
        print(f"\n[meta] {c.metadata}")
        print(f"[text] {c.text}")


if __name__ == "__main__":
    _main()
