set dotenv-load

export EDITOR := 'nvim'

alias f := fmt
alias r := run

default:
  just --list

all: forbid fmt-check lint

dev-deps:
  brew install ruff

forbid:
  ./bin/forbid

fmt:
  isort . && yapf --in-place --recursive .
  prettier --write .

fmt-check:
  isort -c . && yapf --diff --recursive .
  prettier --check .

lint:
  ruff check .

run *args:
  python3 pdfathom {{args}}
