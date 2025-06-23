"""
-*- coding:utf-8 -*-
@Time      :2025/2/18 上午10:38
@Author    :Chen Junpeng

"""
import os
import sys
import datetime
import logging
import functools
import warnings


class LogSettingWarning(UserWarning):
    pass


def log_execution(level=logging.INFO, message="Calling function {func_name} with args: {args} kwargs: {kwargs}"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # try to get logger from args or kwargs
            logger = kwargs.get('logger') or (args[0].logger if args and hasattr(args[0], '__dict__') and 'logger' in args[0].__dict__ else None)

            if logger is None:
                logging.warning("No logger found in arguments, using root logger: %s", str(LogSettingWarning))
                logger = logging.getLogger()

            formatted_message = message.format(func_name=func.__name__, args=args, kwargs=kwargs)
            logger.log(level, formatted_message)

            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator


def default_log_file_name():
    script_name_with_ext = os.path.basename(sys.argv[0])
    script_name = os.path.splitext(script_name_with_ext)[0]
    now = datetime.datetime.now()
    formatted_time = now.strftime("%Y%m%d_%H%M%S")
    log_file = f'./logs/{script_name}_{formatted_time}.log'
    return log_file


def logging_init(log_file: str = None, console_level=logging.DEBUG, file_level=logging.DEBUG, send_to_console=True):
    if not isinstance(log_file, str) or log_file is None:
        log_file = default_log_file_name()

    if not log_file.endswith('.log'):
        log_file += '.log'

    using_log_file = log_file

    if not os.path.exists(os.path.dirname(log_file)):
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        using_log_file = log_file
        warnings.warn(f'logging_init: Path {os.path.dirname(log_file)} does not exist! Creating log file {using_log_file}.', LogSettingWarning)

    if os.path.exists(log_file):
        using_log_file = default_log_file_name()
        warnings.warn(f'logging_init: File {log_file} already exists! Using {using_log_file} instead.', LogSettingWarning)

    print(f'logging_init: Logging to file {using_log_file}.')

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(using_log_file, encoding='utf-8')
    file_handler.setLevel(file_level)

    if send_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(console_level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    if send_to_console:
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    logger.addHandler(file_handler)

    return logger
