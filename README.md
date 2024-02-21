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


## Possible future developements

1. Since the function os.walk(...) already exploits internally (up to Python 3.12.2) a time-consuming call to os.stat() for getting file info, an implementation reusing this call instead of a further one for getting file permissions and size could be explored for improved efficiency.
2. Since getting info on file requires time-consuming, I/O, blocking system calls, an implementation leverage async I/O could be explored.