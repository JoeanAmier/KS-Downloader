FROM python:3.12.4-slim

LABEL name="KS-Downloader" version="1.1" authors="JoeanAmier"

COPY source /source
COPY LICENSE /LICENSE
COPY main.py /main.py
COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
