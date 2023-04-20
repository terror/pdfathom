import argparse
import logging
from dataclasses import dataclass
from typing import List

from .config import Config
from .db import Db, DbConfig
from .repl import Repl

@dataclass
class Arguments:
  pdfs: List[str]
  config: str
  openai_api_key: str
  chunk_size: int
  chunk_overlap: int

  @staticmethod
  def from_args():
    """Parse the command line arguments."""

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

    parser.add_argument(
      "--chunk_size",
      "-s",
      type=int,
      required=False,
      default=1000,
      help="Chunk size",
    )

    parser.add_argument(
      "--chunk_overlap",
      "-o",
      type=int,
      required=False,
      default=0,
      help="Chunk overlap",
    )

    return Arguments(**vars(parser.parse_args()))

  def run(self):
    """Run the REPL."""

    chromadb_logger = logging.getLogger("chromadb")
    chromadb_logger.setLevel(logging.ERROR)

    config = Config.load(self.config)

    if self.openai_api_key:
      config.openai_api_key = self.openai_api_key

    db_config = DbConfig(
      config.openai_api_key, self.chunk_size, self.chunk_overlap
    )

    Repl(Db(db_config).initialize(self.pdfs)).run()
