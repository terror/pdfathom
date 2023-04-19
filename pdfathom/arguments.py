import argparse
from dataclasses import dataclass
from typing import List

from config import Config
from loader import Loader
from repl import Repl

@dataclass
class Arguments:
  pdfs: List[str]
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

    Repl(Loader(config.openai_api_key).load(self.pdfs)).run()
