#coding:utf-8
import logging
import logging.handlers
import os


def log(LogFileName):
    # 初始化日志
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(levelname)-8s %(asctime)s %(filename)s:line:%(lineno)-4d-> %(message)s')
    log_file = os.path.join('Logs', LogFileName)
    file_time_handler = logging.handlers.TimedRotatingFileHandler(log_file, "D", 1, 30)
    file_time_handler.suffix = "%Y%m%d"
    file_time_handler.setFormatter(formatter)
    logger.addHandler(file_time_handler)

    #logger.info(u'调度服务器启动')

    return logger


