#!/usr/bin/bash

../bin/python3 src/main.py > build/template.tex \
&& pdflatex -interaction=nonstopmode -output-directory=build build/template.tex \
&& find build -type f -not -name "template.pdf" -delete
