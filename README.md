# Leaf Grow

A visualisation on leaf grow

## Quickstart

Before you start create a virtual environment and install all dependencies.

To see an example of an animation run:

    python animation.py

To see the outline of a leaf run:

    python path.py


## Before you start

I use a virtual environment so that the dependencies do not mess with dependencies from other projects.

### Create a virtual env

This will create a virtualenv with the python3.6 version and starts it directly.

    mkvirtualenv LeafGrow --python=python3.6

Start the env with

    workon LeafGrow

### Install dependencies


Install the dependencies with

    pip install -r requirements.txt

To add new dependencies install them with 'pip' and then run:

    pip freeze > requirements.txt
