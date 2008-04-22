#!/bin/bash
pylint -f colorized -i y --ignore=tests pyphanfare
python run_tests.py
