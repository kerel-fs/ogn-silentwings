# ogn-silentwings

[![Build Status](https://travis-ci.org/Meisterschueler/ogn-silentwings.svg?branch=master)](https://travis-ci.org/Meisterschueler/ogn-silentwings)
[![Coverage Status](https://img.shields.io/coveralls/Meisterschueler/ogn-silentwings.svg)](https://coveralls.io/r/Meisterschueler/ogn-silentwings)

A connector between  [Open Glider Network](http://wiki.glidernet.org/) and [Silent Wings](http://www.silentwings.no).
The ogn-silentwings module saves all received beacons into a database with [SQLAlchemy](http://www.sqlalchemy.org/).
It connects to the OGN aprs servers with [python-ogn-client](https://github.com/glidernet/python-ogn-client).


## Installation and Setup
1. Checkout the repository

   ```
   git clone https://github.com/Meisterschueler/ogn-silentwings.git
   ```

2. Install python requirements

    ```
    pip install -r requirements.txt
    ```

## Usage

0. Activate virtualenv

    ```
    source venv/bin/activate
    ```

1. Set flask environment

    ```
    export FLASK_APP=flasky.py
    ```

2. Remove previous/outdated data

    ```
    rm data* ;
    ```

3. Create the database

    ```
    flask create_all
    ```

4. Import competition data from strepla

    ```
    # List all available contests from strepla
    flask import_strepla
    flask import_strepla --cID 505
    ```

5. Import task data from strepla

    ```
    # List all tasks
    flask glidertracker_task
    # Download task with taskID 4
    flask glidertracker_task --tID 4
    ```

Online help:
```
Usage: flask [OPTIONS] COMMAND [ARGS]...

  This shell command acts as general utility script for Flask applications.

  It loads the application configured (through the FLASK_APP environment
  variable) and then provides commands either provided by the application or
  Flask itself.

  The most useful commands are the "run" and "shell" command.

  Example usage:

    $ export FLASK_APP=hello.py
    $ export FLASK_DEBUG=1
    $ flask run

Options:
  --version  Show the flask version
  --help     Show this message and exit.

Commands:
  aprs_connect          Run the aprs client.
  create_all            Create the db.
  db                    Perform database migrations.
  glidertracker_filter  Generate a filter list for glidertracker.org
  glidertracker_task    Writes a task in glidertracker format
  import_logfile        Import an OGN APRS stream logfile.
  import_soaringspot    Import data from SoaringSpot.
  import_strepla        Import a StrePla contest from scoring*StrePla
  list_contests_tasks   Lists all contests and tasks from DB
  run                   Runs a development server.
  shell                 Runs a shell in the app context.
  strepla_contests      List all StrePla contests to identify contest...
  test                  Run the unit tests.
```

## License
Licensed under the [AGPLv3](LICENSE).
