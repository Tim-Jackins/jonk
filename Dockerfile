FROM python:3.12

# RUN apt-get install ffmpeg
RUN apt-get update -y
RUN apt-get install -y ffmpeg

COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

COPY ./main.py ./main.py
COPY ./cogs ./cogs

CMD ["python", "main.py"]
