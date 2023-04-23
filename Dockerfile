FROM python:3.10-buster

WORKDIR /app

COPY . /app

RUN python3.10 -m pip install -r requirements.txt

RUN mkdir -p /root/.u2net && \
    wget https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx \
    -O /root/.u2net/u2net.onnx

CMD ["python3.10", "bot.py"]
