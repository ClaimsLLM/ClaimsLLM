import box
import yaml
from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import CTransformers



# Import config vars
with open('config/config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))



# Load docs
def load_docs(directory: str):
    loader = DirectoryLoader(cfg.DATA_PATH,
                             glob='*.pdf',
                             loader_cls=PyPDFLoader)
    documents = loader.load_and_split()
    return documents

#Split docs
def split_docs(documents, chunk_size=1000, chunk_overlap=20):  
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=cfg.CHUNK_SIZE, chunk_overlap=cfg.CHUNK_OVERLAP)
    docs = text_splitter.split_documents(documents)
    return docs

# Build vector database
def run_db_build():
    loader = DirectoryLoader(cfg.DATA_PATH,
                             glob='*.pdf',
                             loader_cls=PyPDFLoader)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=cfg.CHUNK_SIZE,
                                                   chunk_overlap=cfg.CHUNK_OVERLAP)
    texts = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                       model_kwargs={'device': 'cpu'})

    vectorstore = FAISS.from_documents(texts, embeddings)
    vectorstore.save_local(cfg.DB_FAISS_PATH)

def run_db_build_claims():
    loader = DirectoryLoader(cfg.DATA_PATH,
                             glob='*.pdf',
                             loader_cls=PyPDFLoader)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=cfg.CHUNK_SIZE,
                                                   chunk_overlap=cfg.CHUNK_OVERLAP)
    texts = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                       model_kwargs={'device': 'cpu'})

    vectorstore_claims = FAISS.from_documents(texts, embeddings)
    vectorstore_claims.save_local(cfg.DB_FAISS_PATH_CLAIMS)
    

def set_qa_prompt():
    qa_template = """Use the following pieces of information to answer the user's question.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    Context: {context}
    Question: {question}

    Only return the helpful answer below and nothing else.
    Helpful answer:
    """
    prompt = PromptTemplate(template=qa_template,
                            input_variables=['context', 'question'])
    return prompt


    # Local CTransformers model
def build_llm():
    llm = CTransformers(model=cfg.MODEL_BIN_PATH,
                        model_type=cfg.MODEL_TYPE,                        
                        config={'max_new_tokens': cfg.MAX_NEW_TOKENS,
                                'temperature': cfg.TEMPERATURE}
                        )
    return llm



def setup_qachain():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                       model_kwargs={'device': 'cpu'})
    vectordb = FAISS.load_local(cfg.DB_FAISS_PATH, embeddings)
    llm = build_llm()
    qa_prompt = set_qa_prompt()
    qa_chain=RetrievalQA.from_chain_type(llm=llm,
                                       chain_type='stuff',
                                       retriever=vectordb.as_retriever(search_kwargs={'k': cfg.VECTOR_COUNT}),
                                       return_source_documents=cfg.RETURN_SOURCE_DOCUMENTS,
                                       chain_type_kwargs={'prompt': qa_prompt}
                                       )
    
    return qa_chain

def setup_qachain_claims():
    
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                       model_kwargs={'device': 'cpu'})
    vectordb = FAISS.load_local(cfg.DB_FAISS_PATH, embeddings)
    vectordb_claims=FAISS.load_local(cfg.DB_FAISS_PATH_CLAIMS, embeddings)
    vectordb.merge_from(vectordb_claims)
    llm = build_llm()
    qa_prompt = set_qa_prompt()
    qa_chain=RetrievalQA.from_chain_type(llm=llm,
                                       chain_type='stuff',
                                       retriever=vectordb.as_retriever(search_kwargs={'k': cfg.VECTOR_COUNT}),
                                       return_source_documents=cfg.RETURN_SOURCE_DOCUMENTS,
                                       chain_type_kwargs={'prompt': qa_prompt}
                                       )
    
    return qa_chain

   
# if __name__ == "__main__":
#     run_db_build()

