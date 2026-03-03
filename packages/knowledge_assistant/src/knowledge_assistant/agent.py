"""Knowledge Assistant demo brick with lightweight retrieval behavior."""

from __future__ import annotations

from collections import Counter

from common.models import RetrievedDocument
from lfp_logging import logs

LOG = logs.logger()


def _tokenize(text: str) -> list[str]:
    """Convert text into normalized tokens for overlap scoring."""
    return [token.strip(".,!?():;").lower() for token in text.split() if token]


def _overlap_score(query_tokens: list[str], candidate_text: str) -> float:
    """Compute a simple token-overlap score for deterministic demo retrieval."""
    if not query_tokens:
        return 0.0

    candidate_tokens = _tokenize(candidate_text)
    if not candidate_tokens:
        return 0.0

    query_counter = Counter(query_tokens)
    candidate_counter = Counter(candidate_tokens)
    score = 0
    for token, weight in query_counter.items():
        score += min(weight, candidate_counter.get(token, 0))
    return score / max(len(query_tokens), 1)


class KnowledgeAssistantAgent:
    """Retrieves relevant doc chunks and returns a concise answer payload."""

    def retrieve(
        self, query: str, documents: list[dict[str, str]], k: int = 3
    ) -> list[RetrievedDocument]:
        """Select top-k documents for a user question."""
        query_tokens = _tokenize(query)
        ranked_documents: list[RetrievedDocument] = []
        for doc in documents:
            content = doc.get("content", "")
            score = _overlap_score(query_tokens, content)
            if score <= 0:
                continue
            ranked_documents.append(
                RetrievedDocument(
                    doc_id=doc["doc_id"],
                    title=doc["title"],
                    score=score,
                    content=content,
                )
            )

        top_docs = sorted(ranked_documents, key=lambda item: item.score, reverse=True)[
            :k
        ]
        LOG.info("Retrieved %s docs for query=%s", len(top_docs), query)
        return top_docs

    def answer_question(
        self, query: str, documents: list[dict[str, str]]
    ) -> dict[str, object]:
        """Build a deterministic answer object from retrieved evidence."""
        context_docs = self.retrieve(query=query, documents=documents, k=3)
        citations = [doc.doc_id for doc in context_docs]
        evidence = [doc.content for doc in context_docs]

        if not evidence:
            return {
                "question": query,
                "answer": "No relevant documentation was found in the demo corpus.",
                "citations": [],
            }

        answer_text = (
            "Based on the indexed RaceTrac demo documents, here are the key points: "
            + " ".join(evidence[:2])
        )
        return {"question": query, "answer": answer_text, "citations": citations}
