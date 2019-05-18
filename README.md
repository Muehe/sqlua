# sqlua

Unpacks data from the CMaNGOS classic server for addon developers. In Alpha.

## Requirements

1. A full CMaNGOS installation (modified, see below).
    * Optionally a localization.
2. Python3.
3. PyMySQL. Under Linux (Debian/Ubuntu) you can install it like this:  
    ```
    sudo apt-get install pip3
    sudo pip3 install PyMySQL
    ```

## Usage

### Setup

1. Copy the file `main.dist.py` and rename the copy to `main.py`.
    * `main.py` is listed in the gitignore file, so one doesn't accidentally publish ones MySQL credentials.
2. Apply your MySQL information in the `main.py` file.
3. Start IDLE, or another Python 3 interpreter, with sqlua's root as the working directory.
4. Enter the command `from main import *`.
5. Enter the command `printCoordFiles(cursor)`.
6. **Note: Currently you can skip to step 11 at this point.** Modifying CMaNGOS:
  * Working as of:
    * cmangos/mangos-classic@0293535a0b96f4683d02ab230bc728eec84e99bf
    * cmangos/classic-db@6767bf6c3abfade6f8de8efbfdb1ca3dd858e068
  * Go to your `mangos-classic` repository.
  * Make sure you are on the master branch and it is up-to-date:
    * `git checkout master`
    * `git fetch`
    * `git pull`
  * Create and checkout a branch with:
    * `git checkout -b zone`
    * This makes updating CMaNGOS while keeping the patch easier (see below).
  * Apply the patch file:
    * `git apply path/to/sqlua/cmangos.patch`
  * Commit it:
    * `git add .`
    * `git commit -m"CLI: Add Zone and Area command"`
  * Recompile the server.
  * When you update your CMaNGOS later on but want to keep the command do this:
    * `git checkout master`
    * `git fetch`
    * `git pull`
    * `git checkout zone`
    * `git rebase master`
7. Copy the `.csv`-files from the `sqlua/preExtract` directory to the directory containing the `mangosd` executable.
8. Start CMaNGOS.
9. Invoke `server zone FILENAME` in the server console for all the copied files.
10. Copy the files ending in `zone_and_ares.csv` back to the `sqlua/preExtract` directory.
11. Follow one of the extraction methods outlined below.

### Extraction from terminal:

* Invoke `python3 -m main`
* This will start extraction and printing.

### Extraction/Usage from IDLE:

* Start IDLE from sqlua's root directory.
* Enter the command `from main import *`.
* Use the command `main()` to start extraction and printing.
* Use the command `quests, npcs, objects, items = getClassInstances()` to work with the classes from the interpreter.
