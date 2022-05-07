import time

import scripts

if __name__ == '__main__':
    # 提醒班级群小one易打卡
    scripts.one_alert_class(debug=False)
    # 提醒辅导员小one易打卡
    scripts.one_alert_counselor()
    # 延迟退出
    time.sleep(5)
