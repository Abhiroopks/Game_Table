# Game Table

## Overview
* Display future MLB games and associated data

## Setup
1. Create a python virtual environment and install dependencies at the project root.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

2. Run migrations to setup the database.

```bash
python3 manage.py migrate
```

## Running
1. Run the following at the project root to startup the server.

```bash
python3 manage.py runserver
```


## TODO
* Delete games from database that are older than tomorrow (today and before)