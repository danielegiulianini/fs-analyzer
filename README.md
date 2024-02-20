# fs-analyzer

## Intro
A command-line tool that analyzes and reports on the file system structure and usage on a Linux system.

## Features


## How to deploy


### Linux

#### Prerequisites
- Python 3.12.0
- Git (tested with version 2.30.1)
- 
#### Steps


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

5. After exiting the app, remove the container by referring to the name provided before:

```bash
    docker rm <container-name>
```

Then refer to instructions given in the [usage section](#how-to-use).



## How to use


## Hints on future optimizations