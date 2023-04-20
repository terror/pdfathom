**pdfathom** is a command-line utility that lets you query PDF documents with
natural language.

### Installation

You can install it via the pip package manager:

```bash
$ pip install pdfathom
```

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

### Configuration

**pdfathom** looks for a configuration file called `.pdfathom.json` located in
your home directory, and it looks like:

```
{"openai_api_key": "<OPENAI-API-KEY>"}
```

You will be prompted for an OpenAI API key upon running the program if it's not
already present in the configuration file, this will also handle creating the
configuration file for you.
