import logging
import os



from utils.path_tool import get_abs_path
from datetime import datetime
#日志保存的根目录
log_root=get_abs_path("logs")

#确保目录日志存在
os.makedirs(log_root,exist_ok=True)

#日志格式配置
DEFAULT_LOG_FORMAT=logging.Formatter(
    '%(asctime)s - %(name)s -%(levelname)s -%(filename)s:%(lineno)d -%(message)s',
)
"""
%(asctime)s	日志产生的时间	2025-01-15 14:30:22,123
%(name)s	日志记录器的名字（通常是模块名）	root 或 myapp.db
%(levelname)s	日志级别	INFO / WARNING / ERROR
%(filename)s	产生日志的文件名	main.py
%(lineno)d	产生日志的行号	42
%(message)s	你实际写的日志内容	数据库连接成功
"""
def get_logger(
        name:str="agent",
        console_level:int=logging.INFO,
        file_level:int=logging.DEBUG,
        log_file=None
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    #避免重复添加Handler
    if logger.handlers:
        return logger
    #控制台Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)

    logger.addHandler(console_handler)

    #文件Handler
    if not log_file:
        log_file=os.path.join(log_root,f"{name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.log")
    file_handler=logging.FileHandler(log_file,encoding="utf-8")
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)
    logger.addHandler(file_handler)
    return logger
#快捷获得日志管理器
logger=get_logger()

if __name__=="__main__":
    logger.info("信息日志")
    logger.error("错误日志")
    logger.warning("警告日志")
    logger.debug("调试日志")