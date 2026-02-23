import argparse
from src.memory.memory_store import MemoryStore
from src.evaluation.llm_adapter import OllamaLLM
from sklearn.metrics.pairwise import cosine_similarity
from src.retriever.multimodal_router import MultimodalRouter
import numpy as np
import os

mr=MultimodalRouter()
# -------------------------------
# Embedding function (dummy, replace with real)
# -------------------------------
def text_to_embedding(text):
    # For Ollama, you could have a dedicated embedding model if available
    # Here we just mock a random embedding for demonstration
    return np.random.rand(1, 768)

# -------------------------------
# Generate answer
# -------------------------------
def generate_answer(query,chunks, top_k=10):

    memory = MemoryStore()
    last_chats = memory._load()

    context_texts = []
    for c in chunks:

        if isinstance(c, dict):
            for r in c.get("text_results", []):
                txt = r.get("text", "")[:800]
                cid = r.get("chunk_id", "N/A")
                context_texts.append(f"Text Chunk [{cid}]: {txt}")

        elif isinstance(c, str):
            context_texts.append(c[:800])
    chat_history = ""
    for m in last_chats:
        q = m.get("question")
        a = m.get("content")
        chat_history += f"Q: {q}\nA: {a}\n"

    
    user_question = query
    if(mr.is_image(query)):
        for c in chunks:

            if isinstance(c, dict):
                user_question=c.get("caption")
    print("Question asked: ", user_question)

    prompt = f"""
You are an assistant that only answers using the provided context. Do not hallucinate.
If the question is unrelated to the context, respond with "Not found".

Context Chunks:
{chr(10).join(context_texts)}

Chat History (last 5 messages):
{chat_history}

Question: {user_question}

Answer strictly based on the chunks above:
"""

    llm = OllamaLLM()
    answer_text = llm.generate(
        system="You are a helpful assistant.",
        prompt=prompt
    )

    # ----------------------------
    # pick TOP-1 image (if any)
    # ----------------------------
    
        
    top_image = None

    print("\n🖼 TOP IMAGE:\n")

    for c in chunks:
        if isinstance(c, dict):
            imgs = c.get("image_results", [])
            if imgs:
                top_image = imgs[0].get("image_path")
                print("Image:", top_image)
                break   # only first image
        
    # store memory
    # ----------------------------
    memory.add(query, answer_text)

    return {
        "answer": answer_text,
        "image": top_image,
        "chunks": chunks
    }

# -------------------------------
# Compute metrics
# -------------------------------

def compute_metrics(answer, chunks):
    chunk_texts = [c.get("text","") for c in chunks if c["mode"]=="text"]
    if not chunk_texts:
        return {
            "context_match_score": 0.0,
            "faithfulness_score": 0.0,
            "hallucination_detected": True,
            "confidence_score": 0.0
        }

    # Context match
    answer_emb = text_to_embedding(answer)
    chunk_embs = [text_to_embedding(t) for t in chunk_texts]

    # === FIX: flatten 3D embeddings to 2D ===
    if answer_emb.ndim == 3:
        answer_emb = answer_emb.mean(axis=1)  # mean pooling over sequence
    chunk_embs = np.array(chunk_embs)
    if chunk_embs.ndim == 3:
        chunk_embs = chunk_embs.mean(axis=1)  # mean pooling

    context_match_score = max(cosine_similarity(answer_emb, chunk_embs)[0])

    # Faithfulness (simplified heuristic)
    faithfulness_score = 1.0 if "Not found" not in answer else 0.0
    hallucination_detected = faithfulness_score < 0.8
    confidence_score = round((context_match_score + faithfulness_score)/2, 2)

    return {
        "context_match_score": round(context_match_score, 2),
        "faithfulness_score": faithfulness_score,
        "hallucination_detected": hallucination_detected,
        "confidence_score": confidence_score
    }


# -------------------------------
# Full pipeline
# -------------------------------
def context_answer_generator(query, top_k=10):
    result = generate_answer(query, top_k=top_k)

    answer = result["answer"]
    image  = result["image"]
    chunks = result["chunks"]
    metrics = compute_metrics(answer, chunks)
    return {
        "answer": answer,
        "metrics": metrics,
        "chunks_used": chunks,
        "image_used": image
    }

# -------------------------------
# CLI
# -------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("--top_k", type=int, default=10)
    args = parser.parse_args()

    result = context_answer_generator(args.query, args.top_k)
    print("\nAnswer:", result["answer"])
    print("\nMetrics:", result["metrics"])
    print("image used:", result["image_used"])