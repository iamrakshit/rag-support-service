"""TF-IDF embeddings (sparse vectors) fitted on the knowledge base.

Kept dependency-free so the evaluation runs anywhere. The vector store interface does not care how
vectors are produced, so a sentence-transformer model can replace this class without other changes.
"""
import math
from collections import Counter

from .text import tokenize


class TfidfEmbedder:
    def __init__(self, idf=None):
        self.idf = idf or {}

    def fit(self, documents):
        df = Counter(t for d in documents for t in set(tokenize(d, expand=False)))
        n = len(documents)
        self.idf = {t: math.log((1 + n) / (1 + c)) + 1 for t, c in df.items()}
        return self

    def embed(self, text, expand=False):
        tf = Counter(t for t in tokenize(text, expand=expand) if t in self.idf)
        vec = {t: (1 + math.log(c)) * self.idf[t] for t, c in tf.items()}
        norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
        return {t: v / norm for t, v in vec.items()}

    def to_dict(self):
        return {"idf": self.idf}

    @classmethod
    def from_dict(cls, d):
        return cls(d["idf"])


def cosine(a, b):
    if len(a) > len(b):
        a, b = b, a
    return sum(v * b.get(t, 0.0) for t, v in a.items())
