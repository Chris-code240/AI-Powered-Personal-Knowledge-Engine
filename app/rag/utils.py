
from .main import retriever, llm

def rag_query(query: str, top_k: int = 3):
    retrieved_docs = retriever.retrieve(query, top_k=top_k)
    context = "\n".join([doc['text'] for doc in retrieved_docs])

    prompt = f"""
    You are a helpful assistant.
    Use the context below to answer the query. 
    If the answer isn't in the context, say you don't know.

    Context:
    {context}

    Query:
    {query}

    Answer:
    """

    # Step 3: Generate response
    output = llm(
        prompt,
        max_tokens=512,
        temperature=0.7,
        top_p=0.95
    )

    return output["choices"][0]["text"].strip()
