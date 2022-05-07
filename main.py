import time

from message import open_all_windows
from scripts import one

if __name__ == '__main__':
    # 打开所有的qq窗口
    open_all_windows()
    # 提醒班级群小one易打卡
    one.alert_classes()
    # 提醒辅导员小one易打卡
    one.alert_counselors()
    # 延迟退出
    time.sleep(5)
