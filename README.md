# 邓永盛的机器打卡提醒程序

## 概述

基于go-cqhttp，python3，flask，requests，sqlalchemy，MariaDB，docker
+ 旧版本在github上有开源
+ 新版本还没有开源

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
    + counselor  向辅导员发送提醒消息
+ one
    + alert 小one易打卡提醒
    + punch 小one易打卡
+ process-message  接收处理机器人消息
+ schedule-tasks   配置定时任务

## 项目结构

```text
│  .gitignore               # 版本管理忽略文件
│  exceptions.py            # 自定义异常 
│  main.py                  # 主入口
│  Model.DM1                # 数据库模型
│  README.md                # 自述文件
│  requirements.txt         # python依赖文件
│  sql_reverse.bat          # 数据库逆向脚本   
│  test.py                  # 测试文件
├─bin                       #     
├─cube                      # 班级魔方
│      alert_class.py       # 班级提醒
│      auto_punch.py        # 自动打卡
│      request.py           # 网络请求
│      service.py           # 数据库操作
│      update_info.py       # 更新学生信息
├─db                        #    
│      db.py                # 数据库会话
│      models.py            # 数据库模型
├─message                   #
│      config.py            # 消息发送配置
│      message.py           # 消息发送
└─one                       # 小one易
        alert_class.py      # 班级提醒
        alert_counselor.py  # 辅导员提醒    
        auto_punch.py       # 自动打卡
        request.py          # 网络请求
        service.py          # 数据库操作
```

## 待完成工作

- [x] ~~docker容器化，部署到centos~~
- [x] 辅导员提醒
- [ ] 记录启停时间
- [x] 异常记入文件（~~数据库~~）
- [x] **回复消息**，可以根据用户发送的消息进行特定功能部署
- [ ] xml消息，丰富消息样式

## 时间线

+ `2020年11月23日` 立项
+ `2020年11月28日` 项目首次上线
+ `2020年12月7日` 阿里云服务器ip被小one易官方封禁
+ `2021年2月23日` 使用自己的ProxmoxVE虚拟机重新上线
+ `2022年5月5日` 项目重构，使用sqlalchemy框架，增加@功能，改用[go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 进行消息收发，合并晚打卡提醒和小one易统计提醒。
+ `2022年5月8日` 使用mqtt中转消息
+ `2022年5月13日` 早上六点钟前cqhttp崩掉一次，可能是因为断网重连时间过长
+ `2022年5月14日` 重构后上线一周，运行总体稳定
