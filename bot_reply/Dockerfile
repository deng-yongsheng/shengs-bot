FROM python
COPY ./ /app
WORKDIR /app
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && pip3 install -r requirements.txt
CMD python3 main.py process-message
