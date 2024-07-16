FROM python:3.12.4-slim

LABEL name="KS-Downloader" version="1.1 Beta" authors="JoeanAmier"

COPY source /source
COPY LICENSE /LICENSE
COPY main.py /main.py
COPY requirements.txt /requirements.txt

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

CMD ["python", "main.py"]
