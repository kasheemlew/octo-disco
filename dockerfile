FROM python:3.8

WORKDIR /

ADD . .

RUN pip install -r requirements.txt -i https://mirrors.163.com/pypi/simple

CMD export PYTHONPATH="${PYTHONPATH}:." && python garbanzo/main.py