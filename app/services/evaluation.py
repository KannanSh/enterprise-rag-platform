def retrieval_metrics(relevant: list[str], retrieved: list[str]):
    r, got = set(relevant), set(retrieved)
    tp = len(r & got)
    precision = tp / len(got) if got else 0.0
    recall = tp / len(r) if r else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"precision": precision, "recall": recall, "f1": f1}

def citation_coverage(answer: str, retrieved_ids: list[str]):
    if not retrieved_ids: return 0.0
    return sum(1 for cid in retrieved_ids if f"[{cid}]" in answer) / len(retrieved_ids)
