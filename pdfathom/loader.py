import os
from dataclasses import dataclass
from typing import Dict, List
from urllib.request import urlretrieve

from langchain.chains import RetrievalQA
from langchain.chains.retrieval_qa.base import BaseRetrievalQA
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

@dataclass
class Loader:
  openai_api_key: str

  def load(self, pdf_paths: List[str]) -> Dict[str, BaseRetrievalQA]:
    """Load PDFs from paths or URLs and return a dictionary of RetrievalQA objects."""
    return {
      pdf_path: self._build_retriever(self._pdf_path(pdf_path))
      for pdf_path in pdf_paths
    }

  def _pdf_path(self, path: str) -> str:
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
