FROM python
EXPOSE 5701
CMD mkdir /app
WORKDIR /app
COPY ./ /app/
RUN pip3 install -r requirements.txt && pip3 uninstall  --no-input Flask  && pip3 install --no-input Flask
CMD python3 main.py
