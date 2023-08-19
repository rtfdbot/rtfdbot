from dotenv import load_dotenv
load_dotenv()
from llama_index import StorageContext, load_index_from_storage

def getResponse(prompt):
    storage_context = StorageContext.from_defaults(persist_dir="index")

    index = load_index_from_storage(storage_context)
    query_engine = index.as_query_engine()
    response = query_engine.query(prompt)
    return response

def main():
    prompt = "What is the API called for opening space ship doors?"
    result = getResponse(prompt)
    print(result)

if __name__ == "__main__":
    main()