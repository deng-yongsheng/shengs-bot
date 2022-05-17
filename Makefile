FROM = python
target := sheng-bot
exec := docker exec -it $(target) bash -c
exec_d := docker exec -itd $(target) bash -c
cp   := docker cp

.PHONY : docker start clean

docker :
	docker build -t $(target) .
	docker run -itd --name $(target) $(target)

clean :
	docker rm -f $(target)
	docker rmi -f $(target)

test :
	$(exec) "python3 main.py one alert"
