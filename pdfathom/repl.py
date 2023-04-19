import atexit
import os
import readline
from dataclasses import dataclass
from textwrap import dedent
from typing import Dict

from langchain.chains.retrieval_qa.base import BaseRetrievalQA
from rich import print

@dataclass
class Repl:
  HELP = dedent(
    '''
    Enter a query to search the PDF, or type 'exit' to quit.
    Use the up and down arrow keys to navigate through command history.
    Press 'Tab' for command completion suggestions.
  '''
  )

  def __init__(self, retrievers: Dict[str, BaseRetrievalQA]):
    self.retrievers = retrievers
    self.active = list(retrievers.keys())[0]

  def run(self):
    self._init_readline()

    print(f"Active document: [bold]{self.active}[/bold]\n{Repl.HELP}")

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
            print(f"Successfully switched to {self.active := pdf_name}")
          else:
            print(f"{pdf_name} does not exist")
        else:
          print(
            '\n' + dedent(
              self.retrievers[self.active]({
                "query": query
              })["result"].strip()
            ) + '\n'
          )
      except KeyboardInterrupt:
        break
      except Exception as error:
        print(f'error: {error}')

  def _init_readline(self):
    histfile = os.path.expanduser("~/.pdfathom_history")

    try:
      readline.read_history_file(histfile)
    except FileNotFoundError:
      pass

    atexit.register(readline.write_history_file, histfile)
    readline.parse_and_bind("tab: complete")
