# sqlua

Unpacks data from the CMaNGOS classic server for addon developers. In Alpha.

## Requirements

1. A full CMaNGOS classic DB.
    * Optionally a localization.
2. Python3.
3. PyMySQL. With `pip` you can install it like this  
    ```
    pip install -r requirements.txt
    ```  
    It is recommended to add the `--user` option or use virtual environment.

## Usage

### Setup

1. Copy the file `config.py.dist` and rename the copy to `config.py`.
    * `config.py` is listed in the gitignore file, so one doesn't accidentally publish ones MySQL credentials.
2. Apply your MySQL information in the `config.py` file.
3. Follow one of the extraction methods outlined below.

#### Extraction from terminal:

Invoke `python -m main`. This will start extraction and printing, then quit.

#### Interactive usage from interpreter:

1. Start `idle` or `python` in sqlua's root directory.
2. Enter the command `from main import *`.

See `main.py` for the functions you can use.
