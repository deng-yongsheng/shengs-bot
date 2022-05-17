FROM centos
RUN mkdir /app
WORKDIR /app
COPY ./ /app/
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && tar -zxvf go-cqhttp_linux_amd64.tar.gz
EXPOSE 5700
CMD ./go-cqhttp
