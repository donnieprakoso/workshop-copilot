FROM python:3.8.3-slim-buster
WORKDIR /app
COPY app.py /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
EXPOSE 8081
CMD [ "python", "app.py"]
