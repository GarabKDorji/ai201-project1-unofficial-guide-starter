# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->
My system covers student reviews and unofficial advice about UTEP Computer Science courses and professors. This knowledge is valuable because official course descriptions usually explain topics and prerequisites, but they do not show what students actually experience, such as teaching style, workload, grading difficulty, exam expectations, or how helpful a professor is. This information is hard to find through official channels because it is scattered across professor review pages, Reddit threads, and informal student discussions instead of being organized in one searchable place.




---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| #  | Source                                                                                  | Type                             | URL or file path                                                                               |
| -- | --------------------------------------------------------------------------------------- | -------------------------------- | ---------------------------------------------------------------------------------------------- |
| 1  | Daniel Mejia Rate My Professors page                                                    | UTEP CS professor review page    | https://www.ratemyprofessors.com/professor/2665662                                             |
| 2  | Kuldeep Singh Rate My Professors page                                                   | UTEP CS professor review page    | https://www.ratemyprofessors.com/professor/2774250                                             |
| 3  | Monika Akbar Rate My Professors page                                                    | UTEP CS professor review page    | https://www.ratemyprofessors.com/professor/1933020                                             |
| 4  | Ann Gates Rate My Professors page                                                       | UTEP CS professor review page    | https://www.ratemyprofessors.com/professor/225910                                              |
| 5  | Christoph Lauter Rate My Professors page                                                | UTEP CS professor review page    | https://www.ratemyprofessors.com/professor/2989211                                             |
| 6  | Reddit thread: “CS Degree: is it worth it?”                                             | UTEP CS student advice thread    | https://www.reddit.com/r/UTEP/comments/dk5tek/cs_degree_is_it_worth_it/                        |
| 7  | Reddit thread: “Difficulty getting into the CS program?”                                | UTEP CS student advice thread    | https://www.reddit.com/r/UTEP/comments/1kmp26h/difficulty_getting_into_the_cs_program/         |
| 8  | Reddit thread: “How difficult is the Computer Science program?”                         | UTEP CS student advice thread    | https://www.reddit.com/r/UTEP/comments/11n2sth/how_difficult_is_the_computer_science_program/  |
| 9  | Reddit thread: “CS at UTEP or NMSU?”                                                    | UTEP CS comparison/advice thread | https://www.reddit.com/r/UTEP/comments/1abcp64/cs_at_utep_or_nmsu/                             |
| 10 | Reddit thread: “Looking for Honest Opinions on the MS Computer Science Program at UTEP” | UTEP graduate CS advice thread   | https://www.reddit.com/r/UTEP/comments/1fpxuc6/looking_for_honest_opinions_on_the_ms_computer/ |

These are 5 questions the should be able to answer:

     Which UTEP CS professors are described as helpful by students?
     Which UTEP CS professors or courses seem difficult based on student reviews?
     Is the UTEP CS program considered worth it by students?
     What advice do students give before choosing a UTEP CS professor?
     What do students say about workload, support, and opportunities in the UTEP CS program?

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
300 characters (maximum). Most chunks are smaller than this because my real
unit of meaning is one whole student review or one Reddit comment, not a fixed
block of text. I only split a review or comment when it runs longer than 300
characters.

**Overlap:**
100 characters, but only used when a long review/comment has to be split. Short
units are kept whole with no overlap because each one is already a complete
thought. When a long unit is split, the 100-character overlap carries context
across the boundary so a point that lands on the split isn't lost.

**Why these choices fit your documents:**
My documents are mostly short student reviews and Reddit comments, so the
natural unit is one review or one comment — not an arbitrary character window.
I split on the `--- REVIEW ---`, `--- POST ---`, and `--- COMMENT ---` delimiter
lines in each file so that one opinion becomes one chunk. This keeps opinions
from different students or professors from being mixed into the same chunk. 300
characters keeps each chunk focused, which matters because my reviews all use
very similar vocabulary ("clear lectures," "lots of homework," "helpful") — small,
focused chunks retrieve more precisely than large mixed ones.

Preprocessing before chunking:
- Parse the header block at the top of each file (Title, Source, URL, Type,
  Professor) into metadata that travels with every chunk so I can cite the
  correct source.
- Drop `--- POST ---` units: a Reddit post is the thread's *question*, not an
  answer, so indexing it would waste a retrieval slot on a question-shaped chunk.
- Prepend `[Professor: <name>]` to the text of each review. The embedding model
  only sees the chunk text (not the metadata), and the review body never states
  the professor's name, so without this the model can't tell whose review it is.
  Comments are left as-is because they already state their own topic.

**Final chunk count:**
105 chunks total — 59 from the Rate My Professors reviews and 46 from the
Reddit comments.


---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
sentence-transformers/all-MiniLM-L6-v2, run locally through ChromaDB's built-in
SentenceTransformer embedding function. I hand ChromaDB the chunk text and it
produces a 384-dimension vector for each chunk, then uses cosine distance to
find the chunks closest to a query. I chose this model because it is lightweight,
runs locally with no API cost or key, is fast enough for my small corpus (105
chunks), and is the model recommended for this project. For short, informal
student reviews and Reddit comments, its accuracy is more than enough.

**Production tradeoff reflection:**
If I were deploying this for real users and cost was not a constraint, I would
weigh a few tradeoffs before switching models:

- **Accuracy on domain-specific text:** all-MiniLM-L6-v2 is a small general-purpose
  model. A larger model (e.g. all-mpnet-base-v2) or a hosted embedding API
  (e.g. OpenAI text-embedding-3-large, Cohere embed) would likely capture the
  meaning of student slang, sarcasm, and short opinions more accurately, which
  matters here because all my reviews use very similar vocabulary.
- **Context length:** ll-MiniLM-L6-v2 supports inputs of up to 256 tokens. In this project, however, every unit longer than 300 characters is divided into smaller chunks before embedding. A 300-character chunk is normally well below the model’s token limit, so truncation should not be a problem with the current chunking strategy. Context length would become more important if I increased the chunk size or embedded full reviews without splitting them.
- **Latency vs. local control:** a hosted API can be more accurate but adds
  network latency, per-call cost, and sends user questions to a third party.
  Running locally keeps it free, private, and offline, which is why I kept the
  local model for this project.
- **Multilingual support:** my corpus is English-only, so I did not need it. But
  for a multilingual student body, a multilingual model (e.g.
  paraphrase-multilingual-MiniLM) would let students ask questions in Spanish.

For this project the local model wins on cost, privacy, and simplicity; for a
real deployment I would A/B test a stronger hosted model and only pay for it if
it measurably improved retrieval quality on my actual test questions.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
Grounding is enforced both structurally and through the system prompt.

*Structural choice:* The user message sent to the LLM contains the question and the retrieved chunks, formatted as a numbered context block. Each chunk includes a [Source: <professor or thread> | <url>] label constructed from its metadata. The prompt instructs the model to answer only from this retrieved context and not rely on outside knowledge. If the retrieved chunks do not contain enough information, the model must return the specified fallback response.

*System prompt (the actual instruction):* the model is told it answers using
ONLY the retrieved context, with these rules:
- "Answer using ONLY the information in the 'Retrieved context' below. Treat it
  as your entire world of knowledge."
- "Do NOT use any outside or prior knowledge, and do NOT add facts, names,
  courses, or opinions that are not present in the context."
- "Do NOT guess or fill in gaps. If the context does not contain enough
  information to answer, reply exactly: 'I don't have any information regarding
  that.' and nothing else."
- "Report what students actually said, staying close to their specific points...
  do not repeat rude or offensive wording verbatim."

I verified this works: asking "What is the capital of France?" returns "I don't
have any information regarding that." instead of "Paris" — proof the model is
refusing outside (training) knowledge, not just answering from memory. Off-topic
or unknown-professor questions are refused the same way.

**How source attribution is surfaced in the response:**
The model cites its own sources inline. The last system-prompt rule tells it:
"When you do answer, end with a 'Sources:' line listing ONLY the sources you
actually used, copied from the [Source: ...] labels in the context. Do not cite
a source you did not use, and do not invent sources." Because the citation is
generated in the same response as the answer, it always matches what the model
actually used — and when the model refuses, it naturally produces no sources.
Each source line shows the professor (for reviews) or the thread title (for
Reddit comments) plus the original URL, so a user can trace any claim back to the
exact review page or Reddit thread it came from.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What do reviews say about Daniel Mejia's teaching style? | His teaching-style pattern (engaging but work-heavy, "learn by being pushed"); cites Mejia RMP page. | All 5 retrieved chunks were Daniel Mejia reviews (dist 0.35–0.39). Captured both sides: "learn by being pushed" vs lectures "very easy to understand," work-heavy with weekly HW, extra credit. Cited Mejia's RMP page. | Relevant | Accurate |
| 2 | What do reviews say about Kuldeep Singh's course difficulty or workload? | Difficulty/workload/expectations; cites Singh RMP page. | All 5 chunks were Kuldeep Singh reviews (dist 0.39–0.45). CS1320 rated 4–5/5 difficulty, professor assumes prior knowledge, students self-taught via Zybooks. Cited Singh's RMP page. | Relevant | Accurate |
| 3 | What do reviews say about Monika Akbar's helpfulness or class experience? | Whether reviews call her helpful/organized/unclear; cites Akbar RMP page. | All 5 chunks were Monika Akbar reviews (best distances, 0.28–0.33). Lectures "a bit boring but good," very accessible, generous grading, lots of resources. Cited Akbar's RMP page. | Relevant | Accurate |
| 4 | Do students describe the UTEP CS program as worth it? Why or why not? | Main reasons (value, jobs, difficulty, opportunities) from Reddit threads; cites the thread. | Retrieved a mix of the "is it worth it?" and "how difficult?" threads (dist 0.34–0.40). Generally worth it — recognized CS school, Microsoft/Google recruit, but value depends on personal effort. Cited the Reddit threads. | Relevant | Accurate |
| 5 | What advice do students give about succeeding in UTEP CS courses? | Specific advice (choose professors carefully, office hours, practice, prepare for hard exams); cites the source. | Weakest retrieval of the five (dist 0.42–0.47): pulled 3 Mejia reviews + 1 Singh review + 1 Reddit thread rather than explicit "advice" text. Answer inferred advice from those reviews (pick engaging professors, study topics beforehand, expect hard exams) — reasonable but indirect. | Partially relevant | Partially accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

**Summary:** Questions 1–4 performed well. For each professor-related question, all five retrieved chunks were associated with the correct professor, showing the benefit of adding [Professor: ...] directly to the chunk text before embedding. The program-related question also retrieved the appropriate Reddit threads.
Question 5 revealed the system’s main weakness. The query used the broad term “advice,” but none of the documents contained a section that explicitly presented general advice. As a result, it produced the highest distance scores, ranging from 0.42 to 0.47, and retrieved professor-specific reviews rather than dedicated advice content. Although the generated answer was reasonable, it was inferred from the retrieved reviews instead of being directly supported by explicit advice statements. This limitation is analyzed further below.
---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**
Question 5 — "What advice do students give about succeeding in UTEP CS courses?"

**What the system returned:**
Instead of dedicated study advice, retrieval returned 3 Daniel Mejia reviews, 1
Kuldeep Singh review, and 1 Reddit comment — and these came back with the highest
distances of all five questions (0.42–0.47, versus 0.28–0.39 for the professor
questions). The generated answer was plausible but *inferred*: it pieced together
advice from those reviews ("pick professors with engaging lectures," "study the
topics beforehand," "expect difficult exams") rather than reporting advice that a
student explicitly gave.

**Root cause (tied to a specific pipeline stage):**
This is a **retrieval-stage** problem caused by the interaction of my **chunking**
choice and the query. My chunking keeps one review/comment per chunk, and every
chunk is *about a specific professor or a specific thread topic* — none of my
chunks is literally "here is advice for succeeding in CS." The query "advice for
succeeding," on the other hand, is abstract and not phrased like any single chunk.
The embedding model matches on surface meaning, so with no chunk that actually
talks about "advice" in the general sense, the nearest vectors it can find are
professor reviews that merely *mention* studying or exams. The higher distances
(0.42–0.47) are the measurable symptom: the model is telling me "nothing in the
store is really close to this question." So the failure isn't a wrong answer from
the LLM — it's that retrieval had no genuinely on-topic chunk to return, because
advice only exists *implicitly*, spread across many reviews, not concentrated in
any one chunk.

**What you would change to fix it:**
1. **Broaden the corpus:** The most direct improvement would be to add documents that contain explicit advice, such as Reddit threads titled “Tips for CS Majors” or “How to Study for CS Exams.” The retrieval system can only return direct advice when that information exists in the indexed corpus.

2. **Use query expansion or multi-query retrieval:** A broad question about “advice” could be rewritten as several more specific searches, such as “How should students prepare for CS exams?”, “Which professors should students take?”, and “How should students use office hours?” The results from these searches could then be combined. This would help an abstract question match the specific topics discussed in student reviews.

3. **Apply a distance threshold:** Because the best distance score was 0.42, the system could identify the retrieved evidence as relatively weak. Instead of presenting the answer with the same confidence as a strongly supported response, it could tell the user that the answer is based on loosely related reviews or return the fallback response when the distance exceeds a chosen threshold.


---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the specification helped during implementation:**

Writing the chunking strategy in `planning.md` before coding gave me a clear rule to follow: one student review or one Reddit comment should become one chunk. Because I had already identified a single review or comment as the natural unit of meaning, I knew the chunker should split documents using the `--- REVIEW ---`, `--- POST ---`, and `--- COMMENT ---` delimiters instead of blindly dividing the text every fixed number of characters. This decision shaped the entire ingestion process and prevented opinions from different students from being mixed into the same chunk. The specification also established important parameters in advance, including a 300-character chunk size, `top_k = 5`, and the `all-MiniLM-L6-v2` embedding model. As a result, I did not have to stop during implementation to guess these values.

**One way the implementation diverged from the specification, and why:**

The original plan stated that the Reddit thread title would be prepended to every comment so that each comment would retain the context of the question it answered. I initially implemented this approach but removed it after testing. Most comments already described their topic clearly through phrases such as “worth it” or “good program,” allowing them to match relevant queries without an additional thread header. The thread title did not improve retrieval as much as the professor header did. Professor reviews usually do not mention the professor’s name in the review text, so adding `[Professor: ...]` was necessary for distinguishing reviews about different professors. In contrast, adding `[Thread: ...]` to Reddit comments provided little additional value.
A smaller difference was that the original plan emphasized 300-character windows with overlap as the primary chunking method. In the final implementation, delimiter-based splitting became the main mechanism because most reviews and comments were already shorter than 300 characters. Character-based splitting and overlap were only needed for the small number of longer units. Removing the Reddit comment header also affected the final output, resulting in a total of 105 chunks.


---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

Here is a polished version with clearer wording and stronger reflection on your decisions:

**Instance 1 — Chunking and professor/thread headers**

* **What I gave the AI:** I provided the Chunking Strategy section from `planning.md` along with the source documents. I asked it to implement a chunker that loads the files, parses each document’s header block into metadata, and separates the content using the `--- REVIEW ---`, `--- POST ---`, and `--- COMMENT ---` delimiters.

* **What the AI produced:** It generated `chunking.py` with delimiter-based splitting, header parsing, and logic to exclude `--- POST ---` sections from the vector database. It also added a “Fix A” step that prepended `[Professor: ...]` to professor reviews and `[Thread: ...]` to Reddit comments. This identifying information was placed directly in the chunk text because the embedding model processes the text but does not use the metadata when calculating similarity.

* **What I changed or overrode:** I changed the chunk size from 500 to 300 characters because my corpus contains short student reviews and comments rather than long documents. More importantly, I questioned whether the Reddit thread header was necessary. After testing retrieval with and without it, I directed the AI to remove `[Thread: ...]` from comments. Most comments already express their topic through their own wording, so the thread header added extra text without noticeably improving retrieval. I kept `[Professor: ...]` on professor reviews because the review body usually does not include the professor’s name. Including the name in the embedded text was essential for ensuring that professor-specific questions retrieved reviews about the correct professor.

**Instance 2 — How sources are cited in generated answers**

* **What I gave the AI:** I provided the grounding requirements, which stated that answers must use only the retrieved chunks and cite the sources used, along with the existing Gradio `app.py` skeleton.

* **What the AI produced:** It created a version in which the application generated a separate “Retrieved from” panel using the metadata from the retrieved chunks. It also added a string-matching condition that attempted to hide the source panel whenever the model returned the fallback response.

* **What I changed or overrode:** I compared this design with the citation approach used in the RuleBot lab and concluded that the string-matching condition was unnecessarily fragile. It depended on the language model returning the refusal message with exactly the expected wording. I therefore directed the AI to follow the RuleBot approach instead: each retrieved chunk is given a `[Source: ...]` label in the prompt, and the LLM includes the sources it actually uses directly in its response. I removed the separate source panel and the synchronization check. This reduced the amount of application code and made the citations correspond more closely to the evidence used in the generated answer. When the model returns the required fallback response, it naturally provides no source citations.
