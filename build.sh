#!/usr/bin/env bash

# Ensure submodules are initialized
git submodule update --init --recursive

# Proceed with normal build
pip install -r requirements.txt

