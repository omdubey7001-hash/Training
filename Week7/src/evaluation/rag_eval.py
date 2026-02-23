from src.deployment.app import ask,ask_image,ask_sql_query

while True:

    print("\nChoose endpoint:")
    print("1 → /ask")
    print("2 → /ask-image")
    print("3 → /ask-sql")
    print("4 → exit")

    choice = input("Enter: ")

    if choice == "1":
        q = input("Text: ")
        res=ask(q)

    elif choice == "2":
        img = input("Image path: ")
        res=ask_image(img)

    elif choice == "3":
        q = input("SQL question: ")
    
        res=ask_sql_query(q)   
    
    else:
        break



    print("\n===== RAG EVAL =====")
    print("ANSWER:", res["answer"])
    print("IMAGE", res["image"])
    print("CONFIDENCE:", res["confidence"])
    print("HALLUCINATION:", res["hallucination"])
