FROM python:3.8
EXPOSE 8501
WORKDIR /usr/test_project/frontend

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

ENV PYTHONPATH=/usr

CMD ["streamlit", "run", "src/index.py"]
