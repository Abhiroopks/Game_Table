# Game Table

## Overview
* Display weather data for MLB games
* Display MLB games in the next 7 days

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
* Make sure game dates displayed to user use correct timezone
* Add weather data to game records
* Add team standing data to game records