FROM_IMAGE 		:= python
TARGET_NAME 	:= bot-reply
CURRENT_FOLDER 	:= bot_reply
EXEC 			:= docker exec -it $(TARGET_NAME) bash -c
CP 				:= docker cp

.PHONY : docker clean

docker :
	docker run -itd --name $(TARGET_NAME) $(FROM_IMAGE)
	$(EXEC) "mkdir /app"
	$(EXEC) "ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime"
	cd .. && $(CP) ./ $(TARGET_NAME):/app
	$(EXEC) "cd /app && pip3 install -r requirements.txt"

start :
	docker exec -itd $(TARGET_NAME) bash -c "cd /app && python3 main.py process-message"

clean :
	docker rm -f $(TARGET_NAME)
