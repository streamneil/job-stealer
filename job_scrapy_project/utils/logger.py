import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def log(*messages, level='info'):
        """
        记录日志的方法，支持多个字符串参数拼接。
        自动添加当前时间。
        """
        message = ''.join(messages)  # 将所有消息拼接成一个字符串
        if level == 'info':
            logger.info(message)
        elif level == 'error':
            logger.error(message)
        elif level == 'debug':
            logger.debug(message)
        elif level == 'warning':
            logger.warning(message)
        else:
            logger.info(message)  # 默认为info级别