import os
from pathlib import Path
import requests
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
PROJECT_FOLDER = Path(__file__).resolve().parent
PDF_FOLDER = PROJECT_FOLDER / "data" / "pdfs"
PDF_FOLDER.mkdir(parents=True, exist_ok=True)
ALLOWED_PDF_SOURCES = {
    "cs229_linear_algebra": {
        "url": "https://cs229.stanford.edu/section/cs229-linalg.pdf",
        "filename": "cs229_linear_algebra.pdf",
        "label": "Stanford CS229 Linear Algebra Review",
    }
}
COLLECTION_NAME = "capstone_pdf_knowledge_base"
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
client = QdrantClient(":memory:")
client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE,
    ),
)
vector_store = QdrantVectorStore(
    client=client,
    collection_name=COLLECTION_NAME,
    embedding=embeddings,
)
knowledge_base_ready = False
def download_approved_pdf(source_name: str) -> dict:
    """Downloads one approved PDF source to the local data/pdfs folder."""
    if source_name not in ALLOWED_PDF_SOURCES:
        return {
            "success": False,
            "message": "This PDF source is not approved.",
        }
    source = ALLOWED_PDF_SOURCES[source_name]
    file_path = PDF_FOLDER / source["filename"]
    if file_path.exists():
        return {
            "success": True,
            "message": "Approved PDF already exists locally.",
            "file_path": str(file_path),
            "source_url": source["url"],
            "source_label": source["label"],
        }
    response = requests.get(
        source["url"],
        timeout=30,
        headers={"User-Agent": "Day5-Agentic-RAG-Learning-Project"},
    )
    response.raise_for_status()
    content_type = response.headers.get("Content-Type", "").lower()
    if "pdf" not in content_type:
        return {
            "success": False,
            "message": "The approved URL did not return a PDF file.",
        }
    file_path.write_bytes(response.content)
    return {
        "success": True,
        "message": "Approved PDF downloaded successfully.",
        "file_path": str(file_path),
        "source_url": source["url"],
        "source_label": source["label"],
    }
def build_pdf_knowledge_base() -> dict:
    """Downloads the approved PDF, loads pages, chunks text, and stores vectors in Qdrant."""
    global knowledge_base_ready
    if knowledge_base_ready:
        return {
            "success": True,
            "message": "Knowledge base is already ready.",
        }
    download_result = download_approved_pdf("cs229_linear_algebra")
    if not download_result["success"]:
        return download_result
    loader = PyPDFLoader(download_result["file_path"])
    pages = loader.load()
    for page in pages:
        page.metadata["source"] = download_result["source_label"]
        page.metadata["source_url"] = download_result["source_url"]
        page.metadata["page_number"] = page.metadata.get("page", 0) + 1
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=150,
    )
    chunks = splitter.split_documents(pages)
    vector_store.add_documents(chunks)
    knowledge_base_ready = True
    return {
        "success": True,
        "message": "PDF knowledge base was created successfully.",
        "pages_loaded": len(pages),
        "chunks_created": len(chunks),
    }
def search_pdf_knowledge_base(question: str, k: int = 3) -> dict:
    """Searches the approved PDF knowledge base and returns grounded chunks with page citations."""
    if not knowledge_base_ready:
        build_result = build_pdf_knowledge_base()

        if not build_result["success"]:
            return build_result
    results = vector_store.similarity_search_with_score(
        query=question,
        k=k,
    )
    retrieved_chunks = []
    for document, score in results:
        retrieved_chunks.append(
            {
                "content": document.page_content.strip(),
                "source": document.metadata.get("source", "Unknown PDF"),
                "page": document.metadata.get("page_number", "Unknown page"),
                "source_url": document.metadata.get("source_url", ""),
                "similarity_score": round(float(score), 4),
            }
        )
    return {
        "success": True,
        "query": question,
        "retrieved_chunks": retrieved_chunks,
    }
def get_pdf_source_details() -> dict:
    """Returns the approved PDF source information."""
    source = ALLOWED_PDF_SOURCES["cs229_linear_algebra"]
    return {
        "source_name": "cs229_linear_algebra",
        "title": source["label"],
        "url": source["url"],
        "local_file": str(PDF_FOLDER / source["filename"]),
    }