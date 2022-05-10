from_image = python
target_name = mess-forward
exec = docker exec -it $(target_name)
cp = docker cp
expose = -p 5701:5701

.PHONY : docker clean

docker :
	docker run -d --name $(target_name) $(expose) $(from_image)
	$(exec) mkdir /app
	$(cp) ./ $(target_name):/app
	$(exec) cd /app && pip3 install -r requirements.txt && pip3 uninstall  --no-input Flask  && pip3 install --no-input Flask

clean :
	docker rm $(target_name)
