# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
My system covers student reviews and unofficial advice about UTEP Computer Science courses and professors. This knowledge is valuable because official course descriptions usually explain topics and prerequisites, but they do not show what students actually experience, such as teaching style, workload, grading difficulty, exam expectations, or how helpful a professor is. This information is hard to find through official channels because it is scattered across professor review pages, Reddit threads, and informal student discussions instead of being organized in one searchable place.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

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

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
