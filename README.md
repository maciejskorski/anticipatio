![license](https://img.shields.io/pypi/l/fpvgcc.svg?color=blue)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?logo=docker&logoColor=white)
![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?&logo=PyTorch&logoColor=white)
![tests](https://github.com/maciejskorski/anticipatio/actions/workflows/build_test.yml/badge.svg)

# Anticipatio
In a search for understanding of people's anticipation of the future...

## Run / Work with the code 

The Python code requires popular machine-learning Python libraries. 
For convenience, we provide the [Docker file](./Dockerfile) that can be used to run or work with the code.

Build the container with:
```bash
docker build -t anticipatio:dev .
```
Then, run the container mounting this repo directory with 
```bash
docker run --ipc=host --gpus all -it -d -v $(pwd):/home --name anticipatio anticipatio:dev
```
Finally, connect to the container `anticipatio` using your favorite tools, e.g. VS Code extensions. 
