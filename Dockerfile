FROM python:3.6
WORKDIR /usr/src/app
ADD . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "app.py"]

