#!/bin/sh

# Check if pip is installed, and install it if necessary
echo "---- Updating pip ----"
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
echo "---- Pip updated ----"
rm get-pip.py

echo "---- Installing Python Poetry ----"
pip install -U pip
pip install -U poetry
poetry config virtualenvs.in-project true

echo "---- Installing Python dependencies ----"
poetry install

echo "\n\n\n\n\n---- Git hooks init (using mookme) ----"
npm install
npx mookme init --only-hook --skip-types-selection

echo "\n\n\n\n\n---- Your working directory is all set :) ----"
