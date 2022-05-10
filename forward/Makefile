from_image = python
target_name = mess-forward
exec = docker exec -it $(target_name) bash -c
cp = docker cp
expose = -p 5701:5701

.PHONY : docker clean

docker :
	docker run -itd --name $(target_name) $(expose) $(from_image)
	$(exec) "mkdir /app"
	$(cp) ./ $(target_name):/app
	$(exec) "cd /app && pip3 install -r requirements.txt && echo y | pip3 uninstall Flask && pip3 install Flask"

start :
	docker exec -itd $(target_name) bash -c "cd /app && python3 main.py"

clean :
	docker rm -f $(target_name)
