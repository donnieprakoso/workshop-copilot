FROM python:3.8.3-slim-buster
RUN apt-get update
RUN apt-get install wget -y
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb
RUN apt install -y \
                fontconfig \
                libfreetype6 \
                libjpeg62-turbo \
                libpng16-16 \
                libx11-6 \
                libxcb1 \
                libxext6 \
                libxrender1 \
                xfonts-75dpi \
                xfonts-base
RUN dpkg -i wkhtmltox_0.12.6-1.buster_amd64.deb
WORKDIR /app
COPY app.py /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
CMD [ "python", "app.py"]

