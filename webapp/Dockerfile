FROM python:3.8.5-slim

RUN apt-get update && apt-get install libgomp1

COPY ["./requirements.txt", "/usr/src/"]

RUN /usr/local/bin/python -m pip install --upgrade pip

WORKDIR /usr/src

RUN pip install -r requirements.txt

COPY [".","/usr/src/"]

EXPOSE 5000

CMD ["flask", "run","--host=0.0.0.0"]