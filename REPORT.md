# TECH 400 Week 2 Assignment: A Basic Boolean Information Retrieval System

**Student:** Biyush Suwal  
**Institution:** Westcliff University  
**Course:** TECH 400: Introduction to Information Retrieval  
**Instructor / date:** [Add your instructor and submission date]

## Introduction

This project builds a small information retrieval (IR) system that searches eight short descriptions of community activities. A person looking for a local music event, for example, can enter a word or combine two terms with AND or OR. The program shows the documents, the searchable dictionary, the inverted index, and the matching document IDs. This follows the Week 2 requirement to add 5–10 documents, construct a dictionary and inverted index, and implement Boolean retrieval. It also demonstrates the preprocessing and indexing practiced in the Week 2 class activity (Westcliff University, n.d.).

## Design and implementation

I chose eight original, short documents about events in Kathmandu and Bhaktapur. This theme makes it easy to check whether the search results make sense, while keeping the collection small enough to inspect manually. Each document has a unique ID, D1 through D8, and is added with `add_document`. Duplicate IDs are rejected so an existing document cannot silently be overwritten.

Before indexing, `normalize` converts text to lowercase, extracts alphabetic words, removes a short list of common stop words, and applies simple suffix rules. For example, *students* becomes *student*, and *events* becomes *event*. These rules are a demonstration of stemming rather than a full linguistic stemmer; they can produce awkward stems such as *fundrais* and cannot identify every related form. Applying the same normalization to document words and query words lets a search for `students` match indexed *student*. Stop words such as *the* are excluded because they add little meaning to this small example. Manning et al. (2008) describe normalization and dictionary organization as fundamental choices in retrieval systems.

The dictionary is the sorted list of unique normalized terms. The inverted index is a mapping from each term to a **set of document IDs** containing it; for example, `music -> D1, D5`. A set prevents a document from appearing twice when a word repeats. The system creates the index when each document is added, then sorts the dictionary for readable output. A posting list makes retrieval efficient because a query checks relevant document IDs instead of scanning every document each time (Manning et al., 2008).

The `search` method supports one term, `NOT term`, `term AND term`, and `term OR term`. AND finds the intersection of two posting lists, OR finds their union, and NOT subtracts a posting list from all document IDs. Results are sorted to make them predictable. The system rejects other query formats explicitly; it does not support parentheses, phrases, proximity queries, ranked results, or arbitrary Boolean expressions.

## Results and interpretation

Run `python3 ir_system.py` from this folder. The demonstration prints the eight documents, the full index, and these searches:

| Query | Matching IDs | Interpretation |
| --- | --- | --- |
| `music` | D1, D5 | Both descriptions mention music. |
| `local AND music` | D1, D5 | Both contain *local* and *music*. |
| `students OR artists` | D1, D2, D5, D6, D8 | Either normalized term appears. |
| `NOT kathmandu` | D3, D4, D5, D6, D7 | These do not mention Kathmandu. |

For instance, D1 describes students discovering local music events, while D5 describes a local music festival. Their inclusion in `local AND music` demonstrates an intersection. D2 mentions students but not artists, and D8 mentions artists but not students; both correctly appear in the OR result. The NOT query is calculated against the eight-document collection, so every document without *Kathmandu* is returned.

**Screenshot 1 — documents and preprocessing:** [Insert a screenshot of the code showing `samples` and `normalize`, with a caption explaining what is stored and removed.]  
**Screenshot 2 — dictionary and index:** [Insert a screenshot of the terminal from `DICTIONARY AND INVERTED INDEX` through the entries for `local` and `music`; explain that each posting lists matching IDs.]  
**Screenshot 3 — Boolean queries:** [Insert a screenshot of the `BOOLEAN SEARCH` output; explain the AND, OR, and NOT results using the table above.]

## Limitations and conclusion

The example shows the core steps of a Boolean IR system: enter documents, preprocess text, build a term dictionary and inverted index, and retrieve document IDs using set operations. Its small collection makes each result easy to verify. However, Boolean retrieval gives no relevance ranking, and the limited suffix rules can mishandle words. A larger system would use stronger linguistic normalization, persistence, more complete query parsing, and ranked retrieval. Those improvements are outside this Week 2 implementation.

**GitHub repository:** [Paste the public URL after you create and push your repository. Do not submit this placeholder.]

## References

Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to information retrieval*. Cambridge University Press. https://nlp.stanford.edu/IR-book/

Westcliff University. (n.d.). *TECH 400: Introduction to information retrieval* [Course syllabus].

## Submission checklist

1. Run `python3 ir_system.py` and capture your own three screenshots at the marked locations.
2. Replace the cover-page placeholders and paste the screenshots into your final APA 7 document. Use double spacing, 1-inch margins, page numbers, citations, and hanging indents for references.
3. Push `ir_system.py` and this report to your GitHub repository, then replace the GitHub URL placeholder above with the real link.
