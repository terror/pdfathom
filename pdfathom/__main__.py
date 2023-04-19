import sys

from arguments import Arguments
from rich import print

if __name__ == "__main__":
  try:
    Arguments.from_args().run()
  except Exception as error:
    print(f'[bold][red]error[/red]:[/bold] {error}', file=sys.stderr)
    sys.exit(1)
