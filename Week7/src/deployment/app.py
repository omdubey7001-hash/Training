from src.retriever.multimodal_router import MultimodalRouter
from src.retriever.text_to_image import TextToImageRetriever
from src.retriever.image_to_text import ImageToTextRetriever
from src.pipelines.sql_pipeline import ask_sql
from src.memory.memory_store import MemoryStore
from src.generator.query_generator import generate_answer, compute_metrics


rag = MultimodalRouter()
t2i = TextToImageRetriever()
i2t = ImageToTextRetriever()
memory = MemoryStore()



def confidence_score(results):

    # SQL result case → tuple (cols, rows)
    if isinstance(results, tuple):
        cols, rows = results
        if not rows:
            return 0.0
        return 1.0

    # Text RAG case → list[dict]
    if isinstance(results, list) and results:
        if "score" in results[0]:
            return round(results[0]["score"], 3)

    return 0.0


def hallucination_check(answer):

    if not answer:
        return True

    if len(answer) < 5:
        return True

    if "NOT FOUND" in answer.upper():
        return True

    return False


# /ask  (TEXT RAG)

def ask(question, flag=True):

    print("\n=== /ask endpoint ===\n")

    results = rag.run(question)

    context_chunks = [results]

    result = generate_answer(question, context_chunks)

    answer = result["answer"]
    image  = result["image"]
    chunks = result["chunks"]
    metrics = compute_metrics(answer, chunks)
    return {
        "answer": answer,
        "image" : image,
        "confidence": metrics["confidence_score"],
        "hallucination": metrics["hallucination_detected"]
    }



# /ask image

def ask_image(question):

    results = rag.run(question)

    context_chunks = [results]

    result = generate_answer(question, context_chunks)

    answer = result["answer"]
    image  = result["image"]
    chunks = result["chunks"]
    metrics = compute_metrics(answer, chunks)
    return {
        "answer": answer,
        "image" : image,
        "confidence": metrics["confidence_score"],
        "hallucination": metrics["hallucination_detected"]
    }


# /ask-sql

def ask_sql_query(question):

    print("\n=== /ask-sql endpoint ===\n")

    result = ask_sql(question)

    memory.add(question, str(result))
    confidence = confidence_score(result)

    hallucinated = False

    return {
        "answer": result,
        "image": None,
        "confidence": confidence,
        "hallucination": hallucinated
    }


# CLI ROUTER

if __name__ == "__main__":

    while True:

        print("\nChoose endpoint:")
        print("1 → /ask")
        print("2 → /ask-image")
        print("3 → /ask-sql")

        choice = input("Enter: ")

        if choice == "1":
            q = input("Text: ")
            print(ask(q))

        elif choice == "2":
            img = input("Image path: ")
            print(ask_image(img))

        elif choice == "3":
            q = input("SQL question: ")
            print(ask_sql_query(q))
