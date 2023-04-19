import argparse
import atexit
import json
import os
import readline
import sys
import typing as t
from dataclasses import dataclass
from typing import Dict
from urllib.request import urlretrieve

from langchain.chains import RetrievalQA
from langchain.chains.retrieval_qa.base import BaseRetrievalQA
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

@dataclass
class Config:
  openai_api_key: str

  @staticmethod
  def load(config_path: str):
    """Load configuration data from a file or prompt the user for the API key."""
    path = os.path.expanduser(config_path)

    if not os.path.exists(path):
      if (api_key := input("Please enter your OpenAI API key: ")):
        with open(path, "w+") as file:
          file.write(json.dumps({"openai_api_key": api_key}))

    with open(path, "r") as config_file:
      config_data = json.load(config_file)

    return Config(**config_data)

@dataclass
class Loader:
  openai_api_key: str

  def load(self, pdf_paths: t.List[str]) -> Dict[str, BaseRetrievalQA]:
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

@dataclass
class Repl:
  def __init__(self, retrievers: Dict[str, BaseRetrievalQA]):
    self.retrievers = retrievers
    self.active = list(retrievers.keys())[0]

  def run(self):
    histfile = os.path.expanduser("~/.pdfathom_history")

    try:
      readline.read_history_file(histfile)
    except FileNotFoundError:
      pass

    atexit.register(readline.write_history_file, histfile)
    readline.parse_and_bind("tab: complete")

    print(f"Active PDF: {self.active}")
    print("Enter a query to search the PDF, or type 'exit' to quit.")
    print("Use the up and down arrow keys to navigate through command history.")
    print("Press 'Tab' for command completion suggestions.")

    while True:
      try:
        query = input("> ")
        if query.lower() == "exit":
          break
        elif query.lower() == "clear":
          os.system("cls" if os.name == "nt" else "clear")
        elif query.lower().startswith("switch"):
          _, pdf_name = query.split(" ", 1)
          if pdf_name in self.retrievers:
            self.active = pdf_name
            print(f"Switched to PDF: {self.active}")
          else:
            print(f"PDF not found: {pdf_name}")
        else:
          print(self.retrievers[self.active]({"query": query})["result"])
      except KeyboardInterrupt:
        break
      except Exception as error:
        print(f'error: {error}')

@dataclass
class Arguments:
  pdfs: t.List[str]
  config: str
  openai_api_key: str

  @staticmethod
  def from_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
      "pdfs",
      type=str,
      nargs="+",
      help="Path to the pdf file(s) or URL(s)",
    )

    parser.add_argument(
      "--config",
      "-c",
      type=str,
      help="Path to the configuration file",
      default="~/.pdfathom.json",
    )

    parser.add_argument(
      "--openai_api_key",
      "-k",
      type=str,
      required=False,
      help="OpenAI API key",
    )

    return Arguments(**vars(parser.parse_args()))

  def run(self):
    config = Config.load(self.config)

    if self.openai_api_key:
      config.openai_api_key = self.openai_api_key

    retrievers = Loader(config.openai_api_key).load(self.pdfs)

    if not retrievers:
      raise Exception("No PDFs were loaded successfully.")

    Repl(retrievers).run()

if __name__ == "__main__":
  try:
    Arguments.from_args().run()
  except Exception as error:
    print(f'error: {error}', file=sys.stderr)
    sys.exit(1)
