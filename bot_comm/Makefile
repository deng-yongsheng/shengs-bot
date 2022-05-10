from_image = python
target_name = bot-comm
exec = docker exec -it $(target_name) bash -c
cp = docker cp

.PHONY : docker clean

docker :
	docker run -itd --name $(target_name) $(from_image)
	$(exec) "mkdir /app"
	$(cp) ./ $(target_name):/app
	$(exec) "cd /app && pip3 install -r requirements.txt"

start :
	docker exec -itd $(target_name) bash -c "cd /app && python3 main.py process-message"

clean :
	docker rm -f $(target_name)
