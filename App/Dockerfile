FROM python:3.6

RUN apt update && apt upgrade -y && apt install -y cmake
WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["bash"]
