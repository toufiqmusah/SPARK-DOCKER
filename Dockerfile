FROM python:3.11-bullseye

WORKDIR /code

ADD --chmod=755 https://astral.sh/uv/install.sh /install.sh
RUN /install.sh && rm /install.sh

COPY requirements.txt /requirements.txt

RUN /root/.cargo/bin/uv pip install --system --no-cache -r /requirements.txt

ENV LANG C.UTF-8

COPY . /mlcube_project

ENTRYPOINT ["python3", "/mlcube_project/mlcube.py"]
