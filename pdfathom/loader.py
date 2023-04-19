import os
from typing import Dict, List
from urllib.request import urlretrieve

from langchain.chains import RetrievalQA
from langchain.chains.retrieval_qa.base import BaseRetrievalQA
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

class Loader:
  def __init__(self, openai_api_key: str):
    self.openai_api_key = openai_api_key
    self.retrievers: Dict[str, BaseRetrievalQA] = {}
    self.active = None

  def initialize(self, pdf_paths: List[str]):
    """Initialize the loader with a list of PDFs."""

    self.load_documents(pdf_paths)

    if len(pdf_paths):
      self.set_active_document(pdf_paths[0])

    return self

  def documents(self) -> List[str]:
    """Get a list of PDFs."""

    return list(self.retrievers.keys())

  def get_active_document(self) -> str | None:
    """Get the active PDF."""

    return self.active

  def get_active_retriever(self) -> BaseRetrievalQA | None:
    """Get the active retriever."""

    return None if not self.active else self.retrievers[self.active]

  def set_active_document(self, pdf_path: str) -> None:
    """Set the active PDF."""

    self.active = pdf_path

  def has_document(self, pdf_path: str) -> bool:
    """Check if a PDF has been loaded."""

    return pdf_path in self.retrievers

  def load_document(self, pdf_path: str) -> None:
    """Load a PDF from a path or URL.""" ""

    self.retrievers[pdf_path] = self._build_retriever(self._pdf_path(pdf_path))

  def load_documents(self, pdf_paths: List[str]) -> None:
    """Load multiple PDFs from paths or URLs."""

    for pdf_path in pdf_paths:
      self.load_document(pdf_path)

  def _pdf_path(self, path: str) -> str:
    """Return a path to a PDF.""" ""

    return self._download_pdf(
      path
    ) if path.startswith("http") or path.startswith("https") else path

  def _download_pdf(self, url: str) -> str:
    """Download PDF from URL and save it to a temporary file."""

    cache = os.path.expanduser("~/.pdfathom_cache")
    temp_path = os.path.join(cache, os.path.basename(url))
    os.makedirs(os.path.dirname(temp_path), exist_ok=True)
    urlretrieve(url, temp_path)
    return temp_path

  def _build_retriever(self, path: str) -> BaseRetrievalQA:
    """Build a retriever for a PDF."""

    return RetrievalQA.from_chain_type(
      llm=OpenAI(client=None, openai_api_key=self.openai_api_key),
      chain_type="stuff",
      retriever=Chroma.from_documents(
        CharacterTextSplitter(chunk_size=1000, chunk_overlap=0).split_documents(
          PyPDFLoader(path).load_and_split()
        ),
        OpenAIEmbeddings(client=None, openai_api_key=self.openai_api_key),
        persist_directory=os.path.expanduser("~/.pdfathom.db"),
      ).as_retriever(),
      return_source_documents=True,
    )
