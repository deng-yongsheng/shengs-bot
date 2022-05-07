# 邓永盛的机器打卡提醒程序

## 概述

程序依赖于pyautogui，必须在屏幕解锁的情况下运行  
下一步将修改为使用钩子程序控制qq

## 项目结构

```doctest
├─db
│  │  db.py             # 数据库连接配置
│  │  models.py         # orm文件
├─request               # 网络请求相关
│  │  cube.py
│  │  one.py
├─scripts
|  |   auto_punch.py    # 自动打卡入口
|  |   cube.py          # 班级魔方打卡提醒
|  |   one.py           # 小one易打卡提醒
│  exceptions.py        # 自定义异常
│  main.py              # 程序主入口
│  message.py           # 消息发送
│  Model.DM1            # 数据库模型
│  README.md            # 自述文件
│  requirements.txt     # 依赖包
│  service.py           # 数据库相关操作封装
│  sql_reverse.bat      # 数据库逆向脚本
│  test.py              # 测试用例             
```