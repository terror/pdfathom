set dotenv-load

export EDITOR := 'nvim'

alias f := fmt
alias r := run

default:
  just --list

all: forbid fmt-check lint

dev-deps:
  brew install ruff
  cargo install present

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

readme:
  present --in-place README.md

run *args:
  python3 pdfathom {{args}}
