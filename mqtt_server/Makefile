image = rabbitmq
target = rabbitmq
exec := docker exec -it $(target)

.PHONY : docker start_mqtt

docker :
	docker run -itd --restart=always --name $(target) -p 15672:15672 -p 5672:5672 -p 1883:1883 -p 15675:15675 $(image)

start_mqtt :
	$(exec) rabbitmq-plugins enable rabbitmq_management
	$(exec) rabbitmq-plugins enable rabbitmq_mqtt
	# rabbitmq-plugins enable rabbitmq_web_mqtt

clean :
	docker rm -f $(target)
