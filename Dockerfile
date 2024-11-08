FROM python:3.12-slim

WORKDIR /app

LABEL name="KS-Downloader" authors="JoeanAmier" repository="https://github.com/JoeanAmier/KS-Downloader"

COPY source /app/source
COPY LICENSE /app/LICENSE
COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

VOLUME /app

CMD ["python", "main.py"]
