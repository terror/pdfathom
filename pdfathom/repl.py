import atexit
import os
import readline
from dataclasses import dataclass
from textwrap import dedent

from db import Db
from rich import print

@dataclass
class Repl:
  HELP = dedent(
    '''
    Enter a query to search the active PDF document for relevant information.

    [bold]Available commands:[/bold]

    - [green]exit[/green]: Exits the application.
    - [green]clear[/green]: Clears the terminal screen.
    - [green]switch [path or URL][/green]: Switches to another PDF document from a specified path or URL.
    - [green]load [path or URL][/green]: Loads a new PDF document from a specified path or URL.

    [bold]Additional features:[/bold]

    - Use the up and down arrow keys to navigate through command history.
    - Press 'Tab' for command completion suggestions.
    '''
  )

  def __init__(self, db: Db):
    self.db = db

  def run(self) -> None:
    """Start the REPL."""

    self._init_readline()

    print(f'Active document: [bold]{self.db.get_active_document()}[/bold]')

    print(Repl.HELP)

    while True:
      try:
        query = input("> ")

        if query.lower() == "exit":
          break
        elif query.lower() == 'help':
          print(Repl.HELP)
        elif query.lower() == "list":
          self._list()
        elif query.lower() == "clear":
          self._clear()
        elif query.lower().startswith("switch") and len(query.split()) == 2:
          _, pdf = query.split(" ", 1)
          self._switch(pdf)
        elif query.lower().startswith("load") and len(query.split()) == 2:
          _, pdf = query.split(" ", 1)
          self._load(pdf)
        else:
          if (retriever := self.db.get_active_retriever()):
            print(
              '\n' + dedent(retriever({"query": query})["result"].strip()) +
              '\n'
            )
          else:
            print('No active document to query')
      except KeyboardInterrupt:
        break
      except Exception as error:
        print(f'error: {error}')

  def _init_readline(self) -> None:
    """Initialize readline for command history and completion."""

    histfile = os.path.expanduser("~/.pdfathom_history")

    try:
      readline.read_history_file(histfile)
    except FileNotFoundError:
      pass

    atexit.register(readline.write_history_file, histfile)
    readline.parse_and_bind("tab: complete")

  def _clear(self) -> None:
    """Clear the terminal."""

    os.system("cls" if os.name == "nt" else "clear")

  def _switch(self, pdf: str) -> None:
    """Switch to a PDF from a path or URL."""

    if self.db.has_document(pdf):
      self.db.set_active_document(pdf)
      print(f"Successfully switched to {pdf}")
    else:
      if input(
          f"{pdf} does not exist in this context, would you like to load it? [Y/N]: "
      ).lower() == "y":
        self._load(pdf)

  def _load(self, pdf: str) -> None:
    """Load a PDF from a path or URL."""

    if self.db.has_document(pdf):
      print(f"{pdf} is already loaded in this context")
    else:
      self.db.load_document(pdf)
      print(f"Successfully loaded {pdf}")

  def _list(self) -> None:
    """List all loaded PDFs."""

    print(f"Loaded documents: {self.db.documents()}")
