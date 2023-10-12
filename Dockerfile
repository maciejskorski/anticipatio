# BUILD with:
# docker build -t anticipatio:dev .

# RUN with:
# docker run --ipc=host --gpus all -it --rm -v $(pwd):/home --name anticipatio anticipatio:dev

FROM nvcr.io/nvidia/pytorch:23.09-py3

RUN pip install --no-cache-dir kaggle bertopic sklearn

CMD ["bash"]