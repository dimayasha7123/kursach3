FROM python:3.8-slim-buster

WORKDIR /python-docker

COPY req.txt req.txt
RUN pip3 install -r req.txt

ENV FLASK_APP=flaskr
ENV FLASK_ENV=development

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]