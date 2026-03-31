from rag.vectorstore import get_vectorstore

def get_retriever(k=3):
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )
    return retriever

def retrieve_relevant_content(query: str, k=3) -> str:
    retriever = get_retriever(k=k)
    docs = retriever.invoke(query)

    # Join all retrieved chunks into one string
    content = "\n\n---\n\n".join([doc.page_content for doc in docs])

    print(f"🔍 Retrieved {len(docs)} relevant chunks for: '{query}'")
    return content