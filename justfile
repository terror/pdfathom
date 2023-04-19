set dotenv-load

export EDITOR := 'nvim'

alias f := fmt
alias r := run

default:
  just --list

all: forbid fmt-check

forbid:
  ./bin/forbid

fmt:
  isort . && yapf --in-place --recursive .
  prettier --write .

fmt-check:
  isort -c . && yapf --diff --recursive .
  prettier --check .

run *args:
  python3 pdfathom {{args}}
