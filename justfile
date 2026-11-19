# Just is a crossplatform task-runner, similar to make.
# And justfiles are equivalent to makefiles.
#
# Official docs:
#  - https://just.systems/man/en
#
# Usage:
#   > just --help
#   > just <taskname>
#
# Notes:
#  - Comments immediately preceding a recipe will appear in just --list:

# load environment variables from .env file
set dotenv-filename := ".env"
set dotenv-load       := true


# Help target
help:
    @ just --list --unsorted


# create directories
ensure-dirs:
    @ mkdir -p var/cache
    @ mkdir -p var/log
    @ mkdir -p var/run
    @ mkdir -p var/static
    @ mkdir -p var/tmp

# remove generated files and dirs
clean:
    @ rm -fr .venv
    @ rm -fr bin
    @ rm -fr lib 
    @ rm -fr pyvenv.cfg
    
alias clear := clean

# full initial pythondev-installation
install: ensure-dirs create-venv symlink-venv-dirs upgrade-pip uv-sync


# create python39 virtual-environment
create-venv:
    PYENV_VERSION=3.11 python -m venv .venv


# symlink venv-dirs to make bin/python work
symlink-venv-dirs:
    @ ln -sf .venv/bin
    @ ln -sf .venv/lib
    @ ln -sf .venv/pyvenv.cfg


# symlink ipython to ip
symlink-ipython:
    @ cd .venv/bin && ln -sf ipython ip


# upgrade pip itself
upgrade-pip:
    .venv/bin/pip install -U pip


# install the dependencies from uv.lock
uv-sync:
    uv sync --python 3.11


# update uv.lock
uv-lock:
    uv lock


# switch to staging-branch and git pull to update
update-staging:
    git co staging
    git pull
