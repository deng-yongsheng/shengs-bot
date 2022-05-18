# 邓永盛的机器人打卡提醒程序

## 概述

基于go-cqhttp，python3，flask，requests，sqlalchemy，MariaDB，docker。  
使用python的schedule进行定时任务管理，不依赖外部的crontab和操作系统，仅依赖python本身。  
目前在docker容器中运行，完全脱离了windows，效率和稳定性大大提高。除了服务器停电以外，无需人工干预。

+ 目前已经是第三个大版本了
+ 截至2022年5月第二次重构前：
    + 累计发送消息 `49351+` 条
    + 累计提醒 `408412+` 人/次

## 使用

```text
Usage: main.py COMMAND1 COMMAND2 [OPTIONS]

Options:
  --help  Show this message and exit.
```

### command:

+ schedule-tasks 配置定时任务
+ cube
    + alert 班级魔方打卡提醒
    + punch 班级魔方打卡
    + counselor 向辅导员发送提醒消息
+ one
    + alert 小one易打卡提醒
    + punch 小one易打卡
+ process-message 接收处理机器人消息
+ schedule-tasks 配置定时任务

## 项目结构

```text
│  .gitignore
│  config.ini               # 数据库配置文件，使用python的configparser
│  Dockerfile               # docker容器生成脚本
│  exceptions.py            # 项目自定义异常
│  main.py                  # 整个项目的主入口
│  Makefile                 # docker容器管理脚本
│  message_type.py          # qq消息的面向对象封装
│  README.md                # 自述文件
│  requirements.txt         # 项目依赖
│  test.py                  # 单元测试
├─bot_reply
│  │  app.py                # 主启动文件
│  │  bot.py                # 消息接收-回复框架
│  │  mqtt.py               # mqtt客户端
│  │  requirements.txt      # 依赖
│  └─scripts                # 自定义脚本
│          all_groups.py    # 群内消息回复
│          sheng.py         # 特定qq号码的回复
├─cube                      # 班级魔方相关业务
│      alert_class.py       # 班级提醒
│      request.py           # 网络请求
│      service.py           # 数据库查询
│      update_info.py
├─db
│      db.py                # sqlalchemy数据库连接定义
│      models.py            # orm数据库模型
├─forward                   # 消息转发模块
│      config.py            # 消息转发模块的配置项
│      Dockerfile           # docker容器生成脚本
│      main.py              # 主入口
│      Makefile             # docker容器管理脚本
│      requirements.txt     # 依赖库
├─go-cqhttp
│      config.yml           # go-cqhttp的配置文件
│      device.json          # 设备描述
│      Dockerfile           # 生成docker容器
├─message
│      config.py            # 配置文件
│      message.py           # 消息发送api封装
├─mqtt_server               # mqtt docker服务器配置
│      Makefile
└─one #易统计打卡
        alert_class.py      # 发送班级提醒
        alert_counselor.py  # 辅导员提醒
        auto_punch.py       # 班级提醒
        request.py          # 网络请求
        service.py          # 数据库业务封装
```

## 待完成工作

- [ ] 更加完善的日志系统
- [ ] xml消息，丰富消息样式
- [x] ~~docker容器化，部署到centos~~
- [x] ~~辅导员提醒~~
- [x] ~~异常记入文件（数据库~~
- [x] ~~**回复消息**，可以根据用户发送的消息进行特定功能部署~~

## 时间线

+ `2020年11月23日` 立项
+ `2020年11月28日` 项目首次上线
+ `2020年12月7日` 阿里云服务器ip被小one易官方封禁
+ `2021年2月23日` 使用自己的ProxmoxVE虚拟机重新上线
+ `2022年5月5日` 项目重构，使用sqlalchemy框架，增加@功能，改用[go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 进行消息收发，合并晚打卡提醒和小one易统计提醒。
+ `2022年5月8日` 使用mqtt中转消息
+ `2022年5月13日` 早上六点钟前cqhttp崩掉一次，可能是因为断网重连时间过长
+ `2022年5月14日` 重构后上线一周，运行总体稳定
