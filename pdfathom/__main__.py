import sys

from arguments import Arguments

if __name__ == "__main__":
  try:
    Arguments.from_args().run()
  except Exception as error:
    print(f'error: {error}', file=sys.stderr)
    sys.exit(1)
