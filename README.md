**pdfathom** is a command-line utility that lets you query PDF documents with
natural language.

### Installation

You can install it via the pip package manager:

```bash
$ pip install pdfathom
```

### Configuration

**pdfathom** looks for a configuration file called `.pdfathom.json` located in
your home directory, and it looks like:

```
{"openai_api_key": "<OPENAI-API-KEY>"}
```

You will be prompted for an OpenAI API key upon running the program if it's not
already present in the configuration file, this will also handle creating the
configuration file for you.

### Usage

Below is the output of `pdfathom --help`:

```present python3 pdfathom --help
usage: pdfathom [-h] [--config CONFIG] [--openai_api_key OPENAI_API_KEY]
                [--chunk_size CHUNK_SIZE] [--chunk_overlap CHUNK_OVERLAP]
                pdfs [pdfs ...]

positional arguments:
  pdfs                  Path to the pdf file(s) or URL(s)

options:
  -h, --help            show this help message and exit
  --config CONFIG, -c CONFIG
                        Path to the configuration file
  --openai_api_key OPENAI_API_KEY, -k OPENAI_API_KEY
                        OpenAI API key
  --chunk_size CHUNK_SIZE, -s CHUNK_SIZE
                        Chunk size
  --chunk_overlap CHUNK_OVERLAP, -o CHUNK_OVERLAP
                        Chunk overlap
```

A sample run would look like: `pdfathom a.pdf b.pdf https://someurl.com/baz.pdf`
(space-separated) to load in respective PDF files into an interactive REPL
environment (assuming those pdf files exist).

The REPL environment gives you access to a few commands that make it easier to
load and switch to different files:

```
- active: Prints the active PDF document.
- clear: Clears the terminal screen.
- exit: Exits the application.
- help: Displays the help text with available commands.
- list: Lists all loaded PDF documents.
- load <path or url>: Loads a new PDF document from a specified path or URL.
- switch <path or url>: Switches to another PDF document from a specified path or URL.
```
