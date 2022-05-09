#!/usr/bin/python3
import datetime
import os
import time
from typing import List

import click
import schedule

import cube as p_cube
import one as p_one
import messge_process


def gen_time_str_list(s_time: datetime.time, e_time: datetime.time, interval: datetime.timedelta) -> List[str]:
    """
    生成时间序列，精确到分钟
    :param s_time:
    :param e_time:
    :param interval:
    :return:
    """
    start_seconds = s_time.hour * 60 * 60 + s_time.minute * 60 + s_time.minute
    end_seconds = e_time.hour * 60 * 60 + e_time.minute * 60 + e_time.minute
    for i in range(start_seconds, end_seconds, interval.seconds):
        schedule_time = datetime.datetime.fromtimestamp(i, tz=datetime.timezone(datetime.timedelta(hours=0))).strftime(
            '%H:%M')
        yield schedule_time


@click.group()
def cli():
    pass


@cli.command()
def schedule_tasks():
    """
    配置定时任务
    """
    click.echo('配置定时任务')
    # 班级群 班级魔方打卡
    for t in gen_time_str_list(datetime.time(20, 00), datetime.time(23, 40), datetime.timedelta(minutes=15)):
        schedule.every().days.at(t).do(os.system, 'python3 main.py cube alert')
    # 班级群 小one易打卡
    for t in gen_time_str_list(datetime.time(8, 00), datetime.time(22, 00), datetime.timedelta(minutes=60)):
        schedule.every().days.at(t).do(os.system, 'python3 main.py one alert')
    # 小one易辅导员提醒
    schedule.every().days.at('17:00').do(os.system, 'python3 main.py one counselor')
    # 小one易自动打卡
    schedule.every().days.at('07:40').do(os.system, 'python3 main.py one punch')
    # 班级魔方自动打卡
    schedule.every().days.at('20:15').do(os.system, 'python3 main.py cube punch')
    schedule.every().days.at('20:40').do(os.system, 'python3 main.py cube punch')
    all_jobs = schedule.get_jobs()
    print(all_jobs)
    while True:
        schedule.run_pending()
        time.sleep(1)


@cli.command()
def process_message():
    """
    接收机器人消息
    """
    messge_process.app.run(host='0.0.0.0', port='5701')


@cli.group()
def one():
    """
    小one易相关操作
    """
    pass


@one.command()
def punch():
    """
    小one易打卡
    """
    click.echo('小one易打卡')
    p_one.auto_punch()


@one.command()
def alert():
    """
    小one易打卡提醒
    """
    click.echo('小one易打卡提醒')
    p_one.alert_class()


@cli.group()
def cube():
    """
    班级魔方相关操作
    """
    pass


@cube.command()
def alert():
    """
    班级魔方打卡提醒
    """
    click.echo('班级魔方打卡提醒')
    p_cube.alert_class()


@one.command()
def counselor():
    """
    向辅导员发送提醒消息
    """
    p_one.alert_counselor()


@cube.command()
def punch():
    """
    班级魔方打卡
    """
    click.echo('班级魔方打卡')
    p_cube.auto_punch()


if __name__ == '__main__':
    # process_message()
    # p_one.alert_counselor()
    cli()
