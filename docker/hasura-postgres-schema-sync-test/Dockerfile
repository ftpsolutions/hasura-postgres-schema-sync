FROM ubuntu:22.04

RUN apt-get update && apt-get install -y python3 python3-pip

COPY requirements.txt /srv/

WORKDIR /srv/

RUN pip install -r requirements.txt

COPY test.py /srv/test.py

ENTRYPOINT []
CMD ["tail", "-F", "/dev/null"]
