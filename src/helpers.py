from langchain.document_loaders import PyPDFLoader,DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings


#Extract text from PDF files
def load_pdf_files(data):
    loader = DirectoryLoader(
        data,
        glob = "*.pdf",
        loader_cls = PyPDFLoader
    )

    documents = loader.load()
    return documents

#filter the documents to keep only minimal metadata
def filter_to_minimal_doc(docs: List[Document]) -> List[Document]:
    """
    Given a list of Document objects, return a new list of Documents
    containing only the original page_content and minimal metadata:
      - 'source'
      - 'author' (if available: from 'author')
      - 'page' (if available: from 'page', 'page_number', or 'loc.page_number')
    """
    minimal_docs: List[Document] = []
    for doc in docs:
        meta_in = doc.metadata or {}

        # Extract source if present
        source = meta_in.get("source")

        # Extract author if present
        author = meta_in.get("author")

        # Extract page from several common patterns
        page = None
        if "page" in meta_in:
            page = meta_in["page"]
        elif "page_number" in meta_in:
            page = meta_in["page_number"]
        elif isinstance(meta_in.get("loc"), dict) and "page_number" in meta_in["loc"]:
            page = meta_in["loc"]["page_number"]

        # Build minimal metadata dict (omit missing keys)
        meta_out = {}
        if source is not None:
            meta_out["source"] = source
        if author is not None:
            meta_out["author"] = author
        if page is not None:
            meta_out["page"] = page

        minimal_docs.append(
            Document(
                page_content=doc.page_content,
                metadata=meta_out,
            )
        )
    return minimal_docs


#split the documents into smaller chunks
def text_split(minimal_docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 20,
    )
    texts_chunk = text_splitter.split_documents(minimal_docs)
    return texts_chunk

#download embeddings model from huggingface
def download_embeddings():
    """
    Download and Return HuggingFace Embeddings Model
    """
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
    )   
    return embeddings

embedding = download_embeddings()