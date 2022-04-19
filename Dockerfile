FROM python:3.8

WORKDIR /app
COPY . /app

# RUN apt-get install ffmpeg
RUN apt-get update -y
RUN apt-get install -y ffmpeg

RUN pip install pipenv==2018.11.26
RUN pipenv install --deploy --system
RUN pip install git+https://github.com/Tim-Jackins/pafy#egg=pafy

CMD ["python3", "main.py"]
