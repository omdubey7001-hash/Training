import glob
from rank_bm25 import BM25Okapi

from src.retriever.query_engine import search as semantic_search
from src.retriever.merge_utils import merge_and_dedup
from src.retriever.reranker import CrossEncoderReranker
from src.retriever.mmr import MMRSelector
from src.memory.memory_store import MemoryStore



class KeywordRetriever:
    def __init__(self, chunks_path="src/data/chunks"):
        self.chunk_files = glob.glob(f"{chunks_path}/*.txt")
        self.texts = []
        self.file_map = []

        for f in self.chunk_files:
            with open(f, "r", encoding="utf-8", errors="ignore") as fp:
                txt = fp.read()
                self.texts.append(txt)
                self.file_map.append(f)

        tokenized = [t.lower().split() for t in self.texts]
        self.bm25 = BM25Okapi(tokenized)

    def search(self, query, top_k=5):
        query_tokens = query.lower().split()
        scores = self.bm25.get_scores(query_tokens)

        ranked = sorted(
            enumerate(scores),
            key=lambda x: x[1],
            reverse=True
        )[:top_k]

        results = []
        for idx, score in ranked:
            results.append({
                "source": self.file_map[idx],
                "text": self.texts[idx],
                "chunk_id": idx,
                "score": float(score),
                "type": "keyword"
            })

        return results


class HybridRetriever:
    def __init__(self):
        self.keyword = KeywordRetriever()
        self.reranker = CrossEncoderReranker()
        self.mmr = MMRSelector(lambda_param=0.7)
        self.memory = MemoryStore()

    def search(self, query,flag = True, top_k_semantic=5, top_k_keyword=5, final_k=5):
        history_context = self.memory.get_context()
        if history_context:
            print("\nUsing Memory Context...\n")

        enhanced_query = query

        # 1 Semantic Retrieval (FAISS)
        semantic_results = semantic_search(enhanced_query, top_k=top_k_semantic)
        for r in semantic_results:
            r["type"] = "semantic"

        # 2 Keyword Retrieval (BM25)
        keyword_results = self.keyword.search(enhanced_query, top_k=top_k_keyword)

        # 3 Merge + Dedup
        merged = merge_and_dedup(semantic_results, keyword_results)

        if(flag == True): 
            print("\n--- Merged & Deduplicated Results ---\n")
            for i, r in enumerate(merged, 1):
                print(
                    f"{i}. [{r['type']}] {r['source']} | "
                    f"chunk {r.get('chunk_id', 'N/A')} | score {r['score']:.4f}"
                    
                )
                print(r["text"])

        # 4 Cross-Encoder Reranking
        reranked = self.reranker.rerank(
            query=enhanced_query,
            candidates=merged,
            top_k=10
        )

        if(flag == False): 
            print("\n--- Cross-Encoder Reranked ---\n")
            for i, r in enumerate(reranked, 1):
                print(
                    f"{i}. {r['source']} | chunk {r.get('chunk_id', 'N/A')} "
                    f"| rerank_score {r['rerank_score']:.4f}"
                )

        # 5 MMR (Final selection for LLM context)
        final_results = self.mmr.select(
            query=enhanced_query,
            candidates=reranked,
            top_k=final_k
        )

        print("\n--- Final Results after MMR ---\n")
        for i, r in enumerate(final_results, 1):
            print(
                f"{i}. {r['source']} | chunk {r.get('chunk_id', 'N/A')}"
            )
        '''summary_answer = " | ".join([r["source"] for r in final_results[:3]])
        self.memory.add(query, summary_answer)'''

        for r in final_results:
            lines = [l for l in r["text"].split("\n") if "|" not in l]
            r["text"] = "\n".join(lines)

        return final_results



if __name__ == "__main__":
    hr = HybridRetriever()
    q = input("Enter query: ")

    results = hr.search(q)

    print("\n--- Final Context for LLM (After MMR) ---\n")
    for i, r in enumerate(results, 1):
        print(
            f"{i}. SOURCE: {r['source']}\n"
            f"   CHUNK: {r['chunk_id']}\n"
            f"   TEXT: {r['text'][:300]}...\n"
        )

