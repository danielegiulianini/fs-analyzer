# fs-analyzer

## Intro
A command-line tool that analyzes and reports on the file system structure and usage on a Linux system.

## Features


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


6. use the app, referring to instructions given in the [usage section](#how-to-use).


5. After exiting the app, remove the container by referring to the name provided before:

```bash
    docker rm <container-name>
```

## How to use


## Hints on future optimizations