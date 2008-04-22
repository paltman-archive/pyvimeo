#!/bin/bash
pylint -f colorized -i y --ignore=tests pyvimeo
python run_tests.py
