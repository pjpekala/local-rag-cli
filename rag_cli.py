#!.venv/bin/python3.11
import os
from llama_index.core.ingestion import IngestionPipeline, IngestionCache
from llama_index.core.query_pipeline import QueryPipeline
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.cli.rag import RagCLI
from llama_index.llms.ollama import Ollama
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.embeddings.ollama import OllamaEmbedding
import chromadb
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.extractors import TitleExtractor
from llama_index.core import Settings
from llama_index.core.ingestion import IngestionCache

# Set environment variables
os.environ["OPENAI_API_KEY"] = "ollama"
# os.environ["CUDA_VISIBLE_DEVICES"] = "0"  # Ensure we're using the GPU

# Initialize document store and vector store
docstore = SimpleDocumentStore()
chroma_client = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = chroma_client.get_or_create_collection("textbook")

# Define Ollama model for both LLM and embeddings
ollama_model = "llama3.1:8b"

# Initialize Ollama for LLM
llm = Ollama(model=ollama_model, request_timeout=120.0)

# Initialize Ollama for embeddings
embed_model = OllamaEmbedding(model_name=ollama_model)

# Load documents with batching
documents = SimpleDirectoryReader("../OneDrive/Graduate_School/courses/Fall2024/CIS_553/textbook/software_engineering_textbook/", num_files_limit=10).load_data()

# Set up ChromaVectorStore
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

# Set up global settings
Settings.embed_model = embed_model
Settings.llm = llm
Settings.chunk_size = 512
Settings.chunk_overlap = 50

# Create ingestion pipeline with caching
ingestion_cache = IngestionCache(cache_dir="./ingestion_cache")
custom_ingestion_pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=Settings.chunk_size, chunk_overlap=Settings.chunk_overlap),
        TitleExtractor(),
        embed_model
    ],
    vector_store=vector_store,
    docstore=docstore,
    cache=ingestion_cache,
)

custom_query_pipeline = QueryPipeline()

# Create a VectorStoreIndex with batching
batch_size = 50  # Adjusted batch size due to potentially slower embedding process
for i in range(0, len(documents), batch_size):
    batch = documents[i:i+batch_size]
    index = VectorStoreIndex.from_documents(
        batch,
        storage_context=StorageContext.from_defaults(vector_store=vector_store, docstore=docstore),
        show_progress=True
    )

# Create a chat engine
chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

rag_cli_instance = RagCLI(
    ingestion_pipeline=custom_ingestion_pipeline,
    chat_engine=chat_engine,
    llm=llm,
    query_pipeline=custom_query_pipeline,
)

if __name__ == "__main__":
    rag_cli_instance.cli()