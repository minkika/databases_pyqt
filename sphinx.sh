#!/bin/bash
sphinx-apidoc -F --implicit-namespace -o docs/ src/
echo '' >> docs/conf.py
echo 'import os, sys' >> docs/conf.py
echo 'sys.path.insert(0, os.path.abspath(".."))' >> docs/conf.py
echo 'sys.path.insert(0, os.path.abspath("../src/client"))' >> docs/conf.py
echo 'sys.path.insert(0, os.path.abspath("../src/server"))' >> docs/conf.py