FROM python
RUN mkdir /app
COPY  * /app/
WORKDIR /app
RUN python3 -m pip install -r requirements.txt
CMD python3 main.py schedule-tasks
