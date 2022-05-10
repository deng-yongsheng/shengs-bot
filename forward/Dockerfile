FROM fnndsc/ubuntu-python3
EXPOSE 5701
CMD mkdir /app
WORKDIR /app
COPY ./ /app/
RUN pip3 install -r requirements.txt
CMD python3 main.py schedule-tasks
