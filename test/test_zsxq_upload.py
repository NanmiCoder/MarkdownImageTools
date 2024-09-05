import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio

from config import ZSXQ_LOGIN_SUCCESS_COOKEIS
from pkg.zsxq_api_client import ZsxqApiClient

def test_get_uploads_token():
    """
    测试获取上传文件token。
    :return:
    """
    client = ZsxqApiClient(ZSXQ_LOGIN_SUCCESS_COOKEIS)
    token = client.get_uploads_token()
    print(token)


def test_upload_file():
    """
    测试上传文件。
    :return:
    """
    client = ZsxqApiClient(ZSXQ_LOGIN_SUCCESS_COOKEIS)
    upload_res = client.upload_file("/Users/nanmi/Desktop/MediaCrawler源码课程.png")
    print(upload_res)


if __name__ == '__main__':
    test_get_uploads_token()
    test_upload_file()