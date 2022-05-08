FROM python
RUN mkdir /app
COPY  ./ /app/
WORKDIR /app
# 解决时区问题
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && python3 -m pip install -r requirements.txt
CMD python3 main.py schedule-tasks
