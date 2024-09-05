import hashlib
import logging
import random
import time



def init_loging_config():
    level = logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(name)s %(levelname)s (%(filename)s:%(lineno)d) - %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    _logger = logging.getLogger("MarkdownImageTools")
    _logger.setLevel(level)
    return _logger


def genarate_fake_uuid():
    """
    生成一个类似的UUID
    :return:
    """
    result = ""
    for i in range(32):
        # 随机生成一个0-15之间的整数，并转换为十六进制字符串
        result += hex(random.randint(0, 15))[2:]
        # 在指定索引处添加连字符
        if i in [8, 12, 16, 20]:
            result += "-"
    return result



def sha1_encrypt(input_string: str) -> str:
    """
    SHA-1 加密算法
    :param input_string:
    :return:
    """
    # 创建一个 SHA-1 hash 对象
    sha1 = hashlib.sha1()

    # 更新要加密的字符串，注意需要编码成字节类型
    sha1.update(input_string.encode('utf-8'))

    # 获取加密后的十六进制字符串
    return sha1.hexdigest()


def get_timestamp() -> int:
    """
    获取当前时间戳
    :return:
    """
    return int(time.time())


logger = init_loging_config()

