FROM ubuntu
EXPOSE 5701
CMD mkdir /app
WORKDIR /app
COPY ./ /app/
RUN apt update && apt install -y python3 python3-pip && python3 -m pip install -r requirements.txt && pip uninstall jinjia2 && pip install --upgrade jinja2
CMD python3 main.py schedule-tasks