FROM_IMAGE	 		:= python
TARGET_IMAGE		:= bot-reply
TARGET_CONTAINER	:= $(TARGET_IMAGE)
CURRENT_FOLDER	 	:= bot_reply
EXEC 				:= docker exec -it $(TARGET_CONTAINER) bash -c
CP	 				:= docker cp

.PHONY : docker clean

docker :
	cp -f Dockerfile ..
	cd .. && docker build -t $(TARGET_IMAGE) .

start :
	docker run -itd --name $(TARGET_CONTAINER) $(TARGET_IMAGE)

clean :
	docker rm -f $(TARGET_CONTAINER)
	docker rmi -f $(TARGET_IMAGE)
