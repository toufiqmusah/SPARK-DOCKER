FROM python:3.9.16-slim

WORKDIR /mlcube_image

COPY requirements.txt /mlcube_image/requirements.txt

RUN pip3 install --no-cache-dir -r /mlcube_image/requirements.txt

ENV LANG C.UTF-8

COPY ../ /mlcube_image/

ENTRYPOINT ["python3", "/mlcube_image/mlcube.py"]