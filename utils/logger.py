import logging


def logger(log_level='WARN', log_file=None):
    logger = logging.getLogger()
    logger.setLevel(log_level)
    BASIC_FORMAT = "%(asctime)s:%(levelname)s:%(message)s"
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)
    console = logging.StreamHandler()  # 输出到控制台的handler
    console.setFormatter(formatter)
    console.setLevel(log_level)  # 也可以不设置，不设置就默认用logger的level
    print(log_level, log_file)
    if log_file != None:
        file = logging.FileHandler(log_file, encoding='utf-8')  # 输出到文件的handler
        logger.addHandler(file)
        file.setFormatter(formatter)
    logger.addHandler(console)
    return logger
