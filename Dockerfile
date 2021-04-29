FROM python:3.9
WORKDIR /srv/flask_app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY src/ .
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5001"]

