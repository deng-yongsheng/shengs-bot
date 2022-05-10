FROM ubuntu-python3
EXPOSE 5701
CMD mkdir /app
WORKDIR /app
COPY ./ /app/
RUN python3 -m pip install -r requirements.txt && python3 -m pip uninstall jinjia2 && python3 -m pip install --upgrade jinja2
CMD python3 main.py schedule-tasks
