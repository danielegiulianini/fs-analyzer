# fs-analyzer

## Intro
A command-line tool that analyzes and reports on the file system structure and usage on a Linux system.

## Features
1. Directory Traversal: The tool should be able to traverse through a specified directory recursively.
2. File Type Categorization: Classify files into categories (e.g., text, image, executable, etc.) based on their extensions or file signatures.
3. Size Analysis: Calculate and display the total size for each file type category.
4. File Permissions Report: Generate a report of files with unusual permission settings (e.g., world-writable files).
5. Large Files Identification: Identify and list files above a certain size threshold.
6. User Interface: Implement a simple command-line interface where users can specify the directory to be analyzed and set parameters like size threshold.
7. Error Handling: Robust error handling for scenarios like inaccessible directories.

## How to deploy


### Linux

#### Prerequisites
- Git (tested with version 2.30.1)
- Python 3.12.0
- the other dependencies listed in [requirements.txt](./requirements.txt) (before installing these is recommended to create a virtual environment first).

#### Steps
1. clone the repo into the desired folder:

```bash
    git clone https://github.com/danielegiulianini/fs-analyzer
```
2. move inside the downloaded folder:

```bash
    cd fs-analyzer
```

3. create and activate your virtual environment specifying a Python 3.12.0+ interpreter by leveraging the environment manager of choice (e.g., conda, venv).

4. install project dependencies:

```bash
    pip install -r requirements.txt
```

5. use the app by referring to the instructions given in the [usage section](#how-to-use).

6. At the end, possibly deactivate your virtual environment.


### Docker container
#### Prerequisites
- Docker (tested with version 20.10.22)
- Git (tested with version 2.30.1) 

#### Steps
To ease the deployment of the command line demo app a Dockerfile is provided. To use it:

1. clone the repo into the desired folder:

```bash
    git clone https://github.com/danielegiulianini/fs-analyzer
```

2. move inside the downloaded folder:

```bash
    cd fs-analyzer
```

3. build the image of the demo app:

```bash
    docker build -t fs-analyzer-img .
```

4. run the app:

```bash
    docker run -it --name <container-name> fs-analyzer-img
```


6. use the app by referring to the instructions given in the [usage section](#how-to-use).


5. After exiting the app, remove the container by referring to the name provided before:

```bash
    docker rm <container-name>
```

## How to use
After having deployed the project like [explained](#how-to-deploy) and moved to the fs-analyzer\fs_analyzer directory, to use the tool you must specify this syntax at the prompt:

```bash
    python main.py COMMAND [ARGS] ...
``` 

where the commands, along with their (required) arguments are:
```bash

     bigfiles    ROOT_DIR_PATH SIZE     List the files in the directory tree rooted in ROOT_DIR_PATH 
                                        above SIZE (in bytes).
     categorize  ROOT_DIR_PATH          Classify files in the directory tree rooted in ROOT_DIR_PATH 
                                        into mime/types (e.g., text/csv).
     catsizes    ROOT_DIR_PATH          Display the total size per category of files of the directory
                                        tree rooted in ROOT_DIR_PATH.
     fileperms   ROOT_DIR_PATH          List files in the directory tree rooted in ROOT_DIR_PATH with 
                                        unusual permission settings.
```

For general info:
```bash
    python main.py --help             Show an explanatory menu.
```

For info on the specific command:
```bash
    python main.py COMMAND --help     Show an explanatory message for the provided command.
```

### Examples

#### Categorizing files
```bash
     $ python main.py categorize './model'
```

which outputs:
```bash
    filepath        | category
    ------------------------------
    ./model/file_categorization_strategy.py | text/x-python
    ./model/func_utils.py   | text/x-python
    ./model/file_permissions.py     | text/x-python
    ./model/file_category.py        | text/x-python
    ...
```
#### Analyzing file categories' sizes

```bash
     $ python main.py catsizes './model'
```

which outputs:
```bash
    category        | size (B)
    ------------------------------
    FileCategory(name='text/x-python')      | 18245
    FileCategory(name='application/x-python-code')  | 29591
```
#### Reporting unusual permissions

```bash
     $ python main.py fileperms './model'
```

which outputs:
```bash
    filepath        | permissions
    ------------------------------
    ./model/__pycache__/file_listing_generators.cpython-312.pyc     | {'WORLD_EXECUTABLE'}
    ./model/__pycache__/file_generators.cpython-312.pyc     | {'WORLD_EXECUTABLE'}
    ./model/__pycache__/file_permissions.cpython-312.pyc    | {'WORLD_EXECUTABLE'}
    ...
```

#### Listing large files

```bash
     $ python main.py bigfiles './model 1000'
```

which outputs:
```bash
    filepath        | size (B)
    ------------------------------
    ./model/file_listing_generators.py      | 9269
    ./model/__pycache__/file_listing_generators.cpython-312.pyc     | 10174
```

## Possible future developments

1. Since the function [os.walk(...)](https://docs.python.org/3/library/os.html#os.walk) already exploits internally (up to Python 3.12.2) a time-consuming call to [os.stat()](https://docs.python.org/3/library/os.html#os.stat) for obtaining file info, an implementation reusing this call instead of using a separate one could be explored for improved efficiency.
2. As obtaining file information involves time-consuming I/O operations and blocking system calls, an implementation that leverages asynchronous I/O could be explored for improved efficiency. This becomes even more impactful if a file signature is employed for file categorization.
