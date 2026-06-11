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
Most chunks will be one complete student review or one meaningful Reddit comment. Since many reviews are short, some chunks may be under 300 characters. If a review or Reddit comment is long, I will split it into chunks of about 300 characters.

**Overlap:**  
For short reviews/comments, I will use 0 overlap because each one is already a complete unit. For longer comments that need to be split, I will use about 100 characters of overlap.

**Reasoning:**  
My documents are mostly short student reviews and Reddit comments, so the natural unit of meaning is one review or one comment. I do not want to combine many reviews into one large chunk because that could mix opinions from different students or professors. A 300–500 character limit keeps chunks focused, while the overlap helps preserve context when a longer comment is split across two chunks.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**
Retrieval Approach

I will use sentence-transformers/all-MiniLM-L6-v2 as my embedding model because it runs locally, is lightweight, and is recommended for this project. The model will convert both my document chunks and the user’s question into embedding vectors, and ChromaDB will use those vectors to find semantically similar chunks.

**Top-k:**
I plan to retrieve the top 5 chunks for each query. Since my documents are short reviews and Reddit comments, retrieving only 1 or 2 chunks may miss useful student opinions, but retrieving too many chunks could give the LLM noisy or conflicting context. Top-k = 5 gives the model enough evidence while still keeping the context focused.

**Production tradeoff reflection:**
If I were deploying this system for real users and cost was not a constraint, I would compare stronger embedding models based on retrieval accuracy, context length, latency, multilingual support, and whether the model can handle informal student language well. I would also consider whether the model should run locally for privacy/cost reasons or use an API for better performance.


---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question                                                                          | Expected answer                                                                                                                                                                                                                                                                          |
| - | --------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | What do student reviews say about Daniel Mejia’s teaching style?                  | The answer should mention the main teaching-style pattern from the Daniel Mejia reviews, such as whether students describe him as clear, helpful, difficult, organized, or confusing. It should cite the Daniel Mejia Rate My Professors source.                                         |
| 2 | What do student reviews say about Kuldeep Singh’s course difficulty or workload?  | The answer should summarize what Kuldeep Singh reviews say about difficulty, workload, assignments, exams, or expectations. It should cite the Kuldeep Singh Rate My Professors source.                                                                                                  |
| 3 | What do student reviews say about Monika Akbar’s helpfulness or class experience? | The answer should identify whether reviews describe Monika Akbar as helpful, challenging, organized, unclear, or supportive, based only on the collected reviews. It should cite the Monika Akbar Rate My Professors source.                                                             |
| 4 | Do students describe the UTEP CS program as worth it? Why or why not?             | The answer should summarize the main reasons students give in the UTEP CS Reddit threads, such as program value, difficulty, resources, professors, projects, or opportunities. It should cite the relevant Reddit thread.                                                               |
| 5 | What advice do students give about succeeding in UTEP CS courses?                 | The answer should mention specific advice found in the Reddit threads or professor reviews, such as choosing professors carefully, practicing outside class, using office hours, doing projects, or preparing for difficult courses. It should cite the source where the advice appears. |


---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

## Anticipated Challenges

1. One challenge is separating the raw data into useful chunks. Since my sources are mostly individual reviews and Reddit comments, I want each review or meaningful comment to stay together as one chunk. However, some comments may be longer than my target chunk size, so important context could get split across chunks. I will handle this by using overlap for longer comments so the retrieved chunk still has enough context.

2. Another challenge is noisy or incomplete student-generated text. Some reviews may not include course numbers, professor names, or clear details, and some Reddit comments may contain slang, sarcasm, or inappropriate language. This could make retrieval less accurate or make the generated answer sound unprofessional. To reduce this risk, I will keep useful metadata like source, professor name, course if available, and URL, and I will instruct the LLM to summarize the meaning professionally instead of copying rude or informal wording directly.
---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

```text
Raw Documents
(Rate My Professors reviews + Reddit CS advice threads)
        |
        v
Document Ingestion
(load .txt files from data/raw, clean text, keep metadata)
        |
        v
Chunking
(one review/comment per chunk; split long comments around 300–500 characters with overlap)
        |
        v
Embedding + Vector Store
(sentence-transformers/all-MiniLM-L6-v2 creates embeddings;
ChromaDB stores chunk vectors and metadata)
        |
        v
Retrieval
(user query is embedded; retrieve top 5 most similar chunks from ChromaDB)
        |
        v
Generation
(Groq llama-3.3-70b-versatile generates a grounded answer using retrieved chunks only)
```


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

## AI Tool Plan

I plan to use ChatGPT mainly as a tutor and debugging helper. I will use it to understand the RAG workflow, explain what different functions are doing, pressure-test my design choices, and help me paraphrase documentation in my own words. I will use Claude/Copilot to help implement specific parts of the pipeline one milestone at a time, using my planning.md and architecture diagram as the input. I will not ask AI to generate the whole project at once. I will check each part by running it, printing outputs, and comparing the behavior to my project plan.

**Milestone 3 — Ingestion and chunking:**
I will give Claude/Copilot my Documents section, Chunking Strategy section, and Architecture diagram. I expect it to help me write code that loads the raw .txt files from data/raw/, keeps metadata such as source, URL, professor name, and course if available, and splits the text into review/comment-based chunks. I will verify the output by printing sample chunks and checking that each chunk contains one complete review or meaningful Reddit comment. For long comments, I will check that they are split using my 300–500 character target with overlap.

**Milestone 4 — Embedding and retrieval:**
I will give Claude/Copilot my Retrieval Approach section and ask it to help connect sentence-transformers/all-MiniLM-L6-v2 with ChromaDB. I expect it to produce code that embeds each chunk, stores the chunk text and metadata in ChromaDB, embeds the user query, and retrieves the top 5 most similar chunks. I will verify this by running test queries and checking whether the retrieved chunks actually match the question before adding generation.

**Milestone 5 — Generation and interface:**
I will give Claude/Copilot my Architecture diagram, Retrieval Approach, and the project requirement that answers must be grounded and cited. I expect it to help me write a function that sends only the retrieved chunks to the Groq LLM and generates an answer with source attribution. I will verify this by running my 5 evaluation questions, checking the retrieved chunks, making sure the answer cites the correct source, and confirming the response does not include unsupported information outside the documents.