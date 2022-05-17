target := go-cqhttp
exec := docker exec -it $(target) bash -c
exec_d := docker exec -itd $(target) bash -c
cp   := docker cp

.PHONY : docker test start clean

docker :
	docker build -t $(target) .
	docker run -itd --name $(target) -p 5700:5700 $(target)
	$(exec) "ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime"
	# 复制文件
	$(cp) ./ $(target):/app
    # 解压文件
	$(exec) "cd /app && tar -zxvf go-cqhttp_linux_amd64.tar.gz"

test :
	$(exec) "cd /app && /app/go-cqhttp"

start :
	$(exec_d) "cd /app && /app/go-cqhttp"

clean :
	docker rm -f $(target)


