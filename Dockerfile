# app/Dockerfile

FROM python:3.9-slim

EXPOSE 8501

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

# RUN git clone https://github.com/streamlit/streamlit-example.git .

COPY . /app



COPY DataApp/config.ini /app/DataApp 

WORKDIR /app/DataApp
ENV PYTHONPATH=../
ENTRYPOINT ["streamlit", "run", "stramlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
