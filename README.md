**pdfathom** is a command-line utility that lets you query PDF documents with
natural language.

### Installation

You can install it via the pip package manager:

```bash
$ pip install pdfathom
```

### Usage & Configuration

Below is the output of `pdfathom --help`:

```
usage: pdfathom [-h] [--config CONFIG] [--openai_api_key OPENAI_API_KEY] pdfs [pdfs ...]

positional arguments:
  pdfs Path to the pdf file(s) or URL(s)

options:
  -h, --help Show this help message and exit
  --config CONFIG, -c CONFIG Path to the configuration file
  --openai_api_key OPENAI_API_KEY, -k OPENAI_API_KEY OpenAI API key
```

You will be prompted for an OpenAI API key upon running the program if it's not
already present in `~/.pdfathom.json`.
