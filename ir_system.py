"""TECH 400 Week 2: small Boolean information retrieval system."""

import re
from collections import defaultdict


STOP_WORDS = {"a", "an", "and", "are", "for", "in", "is", "of", "on", "the", "to"}


def normalize(text):
    """Lowercase, tokenize, remove stop words, and apply simple suffix rules."""
    tokens = re.findall(r"[a-z]+", text.lower())
    result = []
    for token in tokens:
        if token in STOP_WORDS:
            continue
        if token.endswith("ies") and len(token) > 4:
            token = token[:-3] + "y"
        elif token.endswith("ing") and len(token) > 5:
            token = token[:-3]
        elif token.endswith("s") and not token.endswith("ss") and len(token) > 3:
            token = token[:-1]
        result.append(token)
    return result


class RetrievalSystem:
    def __init__(self):
        self.documents = {}
        self.index = defaultdict(set)

    def add_document(self, doc_id, text):
        if doc_id in self.documents:
            raise ValueError(f"Duplicate document ID: {doc_id}")
        self.documents[doc_id] = text
        for term in set(normalize(text)):
            self.index[term].add(doc_id)

    def search(self, query):
        """Accept TERM, TERM AND TERM, TERM OR TERM, and NOT TERM."""
        parts = query.upper().split()
        if not parts:
            raise ValueError("Query cannot be empty")
        operators = {"AND", "OR", "NOT"}
        if len(parts) == 2 and parts[0] == "NOT":
            return sorted(set(self.documents) - self._postings(parts[1]))
        if len(parts) == 1 and parts[0] not in operators:
            return sorted(self._postings(parts[0]))
        if len(parts) == 3 and parts[1] in {"AND", "OR"}:
            left, right = self._postings(parts[0]), self._postings(parts[2])
            return sorted(left & right if parts[1] == "AND" else left | right)
        raise ValueError("Use TERM, NOT TERM, TERM AND TERM, or TERM OR TERM")

    def _postings(self, term):
        tokens = normalize(term)
        if len(tokens) != 1:
            raise ValueError(f"Query term must contain one non-stop word: {term}")
        return self.index.get(tokens[0], set())


if __name__ == "__main__":
    system = RetrievalSystem()
    samples = {
        "D1": "Students discover local music events in Kathmandu.",
        "D2": "A Kathmandu cafe hosts a fundraising event for students.",
        "D3": "Local schools organize sports events for children.",
        "D4": "Community volunteers promote a health camp in Bhaktapur.",
        "D5": "A music festival raises funds for local artists.",
        "D6": "Students attend a technology workshop in Bhaktapur.",
        "D7": "Local organizations host fundraising campaigns for schools.",
        "D8": "A community art event brings artists to Kathmandu.",
    }
    for doc_id, text in samples.items():
        system.add_document(doc_id, text)

    print("DOCUMENTS:")
    for doc_id, text in system.documents.items():
        print(f"{doc_id}: {text}")
    print("\nDICTIONARY AND INVERTED INDEX:")
    for term, posting in sorted(system.index.items()):
        print(f"{term:15} -> {', '.join(sorted(posting))}")
    print("\nBOOLEAN SEARCH:")
    for query in ["music", "local AND music", "students OR artists", "NOT kathmandu"]:
        print(f"{query:22} -> {system.search(query)}")
