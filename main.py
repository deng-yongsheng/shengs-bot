import datetime
import time
from typing import List

import click
import schedule

import cube as p_cube
import one as p_one


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
    # 提醒班级群小one易打卡
    for t in gen_time_str_list(datetime.time(20, 00), datetime.time(23, 40), datetime.timedelta(minutes=15)):
        schedule.every().days.at(t).do(p_one.alert_class, False)
    # 提醒班级群班级魔方打卡
    for t in gen_time_str_list(datetime.time(8, 00), datetime.time(22, 00), datetime.timedelta(minutes=60)):
        schedule.every().days.at(t).do(p_cube.alert_class, False)
    # 小one易自动打卡
    schedule.every().days.at('07:40').do(p_one.auto_punch)
    # 班级魔方自动打卡
    schedule.every().days.at('08:40').do(p_cube.auto_punch)
    all_jobs = schedule.get_jobs()
    print(all_jobs)
    while True:
        schedule.run_pending()
        time.sleep(1)


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


@cube.command()
def punch():
    """
    班级魔方打卡
    """
    click.echo('班级魔方打卡')
    p_cube.auto_punch()


if __name__ == '__main__':
    cli()
