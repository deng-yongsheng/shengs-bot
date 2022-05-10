FROM ubuntu
CMD mkdir /app
WORKDIR /app
COPY ./ /app/
RUN apt update && apt install -y python3 python3-pip && python3 -m pip install -r requirements.txt
CMD python3 main.py schedule-tasks