FROM python
RUN mkdir /app
COPY  * /app/
WORKDIR /app
RUN timedatectl set-timezone Asia/Shanghai && python3 -m pip install -r requirements.txt
CMD python3 main.py schedule-tasks
