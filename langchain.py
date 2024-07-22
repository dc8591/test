2"""Endpoint"""

@app.route('/lang-chat', methods=["POST"])
def lang_chat():
   
    return handle_request(knowledge_chat)


"""Chat function"""
def knowledge_chat(request_params):
    try:
        start_time = time.time()
        required_params = ["query", "chat_history"]
        if any(param not in request_params for param in required_params):
            return {"data": {}, "status": False, "message": "Required parameters missing",}, 400
        
        question = request_params.get("query")
        chat_history = request_params.get("chat_history") 
        session_id = request_params.get("session") 
        # chat_history_data = []
        # chat_history_data.extend(
        #     mongo_manager.find_many(
        #         os.getenv("MONGO_DB_NAME"),
        #         "chat_history_collection",
        #         {"session_id":session_id},
        #         projection={"_id": 0, "human_message": 1, "ai_message":1}
        #     )
        # )

        # for data in chat_history_data:
        #     human_message = HumanMessage(content=data.get("human_message"))
        #     ai_message = AIMessage(content=data.get("ai_message"))
        #     chat_history.append(human_message)
        #     chat_history.append(ai_message)

        print(chat_history)
        
        base_dir = os.path.dirname(os.path.abspath(__file__))  # directory of the script
        knowledge_base_path = os.path.join(base_dir, "hyundai-knowledge-base-v005")
        retriever = Chroma(persist_directory=knowledge_base_path, embedding_function=OpenAIEmbeddings(model="text-embedding-ada-002"),)
        retriever_chain = get_context_retriever_chain(retriever)
        conversation_rag_chain = get_conversational_rag_chain(retriever_chain)

        response = conversation_rag_chain.invoke({
            "chat_history": chat_history,
            "input": question
        })

        # mongo_manager.insert_one(
        #         os.getenv("MONGO_DB_NAME"),
        #         "chat_history_collection",
        #         {
        #             "session_id":session_id,
        #             "human_message": question, 
        #             "ai_message":response['answer']
        #         },
        #     )
        # chat_history.append(HumanMessage(content=question))
        # chat_history.append(AIMessage(content=response['answer']))
        
        print(response['answer'])
        print(f"excecution time is {time.time()-start_time} ")
        return {"data": {"result": response['answer'],}, "status": True, "message": "Success",}, 200
    except:
        return {"data": {"result": "¿Podrías repetirlo, por favor?",}, "status": True, "message": "Success",}, 200




"""Create embeddings"""
import requests
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings


def get_response_and_save(url):
    
    loader = WebBaseLoader(url)
    document = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter()
    document_chunks = text_splitter.split_documents(document)
    
    vector_store = Chroma.from_documents(document_chunks, OpenAIEmbeddings(model="text-embedding-ada-002"), persist_directory="./hyundai-knowledge-base-v005")
    print(f"Embeddings created for {url}")
    return True

###--------------------------------------------------------------------------###

import json
def get_scrapped_data(params):
    f = open('modelos\sitemap.json')
    data = json.load(f)
    
    scrapped_data_urls = [get_response_and_save(data[url]) for url in data]  
    print("Embeddings created for models")
    f.close()

if __name__ == '__main__':
    params = None
    get_scrapped_data(params)
            
    

