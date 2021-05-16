FROM python:3.8

WORKDIR /usr/test_project/backend
RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

ENV PYTHONPATH=/usr
ENV FLASK_APP=app.py

CMD ["python3", "manage.py", "run", "--host=0.0.0.0"]
# CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
