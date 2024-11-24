#!/usr/bin/bash

python3 src/main.py > build/template.tex && pdflatex -interaction=nonstopmode -output-directory=build build/template.tex
