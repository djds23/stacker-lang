#!/usr/bin/env bash

rm -rf dist/
python setup.py sdist bdist_wheel
TWINE_REPOSITORY_URL=https://upload.pypi.org/legacy/ twine upload dist/*
