# Cocktail Dataset

Cocktails in this repository are sourced from [101 Girly Drinks](https://www.amazon.com/101-Girly-Drinks-Cocktails-Occasion/dp/1780973837).
Recipes follow the [Open Recipe Format](https://github.com/techhat/openrecipeformat).
The intent is to enable data analytics on recipes, and play with AWS, because why not?

## Equipment Assumptions

We assume you have unlimited access to the following when using this dataset: ice, blender, martini glass, highball glass, margarita glass, shaker tin.

# Quick Start

Execute `scripts/setup.sh` from the project root.
This script creates the virtualenvironment and prints an example invocation of the program for local testing.
Failure to exeucte this script from the project root will **not** detect the current version of Python.

## Contributing

Install the requirements in `dev-requirements.txt` if you want to run linters locally before pushing.

# Data Processing

Ingest recipe files using whatever format you prefer.
I'm comfortable with `pandas`, so that's what you see in `main.py`.