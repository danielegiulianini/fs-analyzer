FROM python:3.12-alpine

ADD requirements.txt ./

RUN pip install --upgrade pip

COPY . ./app

RUN pip install -r requirements.txt

WORKDIR /app/fs_analyzer

CMD ["/bin/sh"]