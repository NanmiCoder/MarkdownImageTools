
# -*- coding: utf-8 -*-
import logging

import httpx

logger = logging.getLogger(__name__)


class SyncHTTPClient:
    def __init__(self, base_url: str = ""):
        self.client = httpx.Client()
        self.base_uri = base_url

    def __enter__(self):
        """
        在进入同步上下文管理器时调用。
        返回实例自身，允许在'with'块中使用。
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        在退出同步上下文管理器时调用。
        无论是否发生异常，都将关闭HTTP客户端。
        """
        self.close()

    def fetch(self, method: str, url: str, **kwargs):
        """
        执行HTTP请求。
        :param method: HTTP方法，如'GET'或'POST'。
        :param url: 请求的URL。
        :param kwargs: 传递给httpx请求的额外参数。
        :return:
        """
        if self.base_uri:
            url = self.base_uri + url
        logger.info(f"Request started: {method} {url}, kwargs:{kwargs}")
        try:
            response = self.client.request(method, url, **kwargs)
            logger.info(f"Request completed with status {response.status_code}")
            return response
        except Exception as e:
            logger.error(f"Request failed: {str(e)}")
            raise

    def get(self, url: str, **kwargs):
        """
        发送GET请求。
        :param url: 请求的URL
        :param kwargs: 传递给httpx请求的额外参数。
        :return:
        """
        return self.fetch('GET', url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        """
        发送POST请求。
        :param url: 请求的URL。
        :param data: 用于表单数据的字典。
        :param json: 用于JSON数据的字典。
        :param kwargs: 传递给httpx请求的额外参数。
        :return:
        """
        if json is not None:
            kwargs['json'] = json
        elif data is not None:
            kwargs['data'] = data
        return self.fetch('POST', url, **kwargs)

    def close(self):
        """
        关闭HTTP客户端。
        """
        self.client.close()
