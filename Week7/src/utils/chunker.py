from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_text(text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,      # max size
        chunk_overlap=100    # overlap
    )
    return splitter.split_text(text)
