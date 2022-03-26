FROM python:3.10.2-slim-buster

COPY ./requirements.txt /root/requirements.txt

RUN pip install --upgrade pip && \
    pip install --ignore-installed -r /root/requirements.txt

WORKDIR /root/docker

COPY . /root/docker

CMD ["python", "main.py"]