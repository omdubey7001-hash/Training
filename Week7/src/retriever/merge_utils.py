def merge_and_dedup(semantic_results, keyword_results):
    """
    semantic_results: list of dicts from FAISS
    keyword_results: list of dicts from BM25
    """

    merged = {}

    for r in semantic_results:
        key = (r["source"], str(r["chunk_id"]))
        merged[key] = r

    for r in keyword_results:
        fname = r["source"].split("/")[-1]

        if "_chunk_" not in fname:
            continue

        source_file = fname.split("_chunk_")[0] + ".txt"
        chunk_id = fname.split("_chunk_")[1].replace(".txt", "")

        key = (source_file, chunk_id)

        if key not in merged:
            merged[key] = {
                "source": source_file,
                "chunk_id": chunk_id,
                "text": r["text"],
                "score": r["score"],
                "type": "keyword"
            }

    return list(merged.values())
