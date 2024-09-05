import random
from abc import ABC, abstractmethod
from time import sleep

import config
import constant
import utils
from pkg.zsxq_api_client import ZsxqApiClient


class BaseUploader(ABC):
    @abstractmethod
    def upload(self, file_path: str):
        pass


class AliyunUploader(BaseUploader):
    def upload(self, file_path: str):
        # Implement Aliyun upload logic here
        # Return the URL of the uploaded image
        utils.logger.info(f"Uploading image to Aliyun, local path: {file_path}")
        sleep(random.Random().randint(1, 3))
        return file_path


class QiniuUploader(BaseUploader):
    def upload(self, file_path: str):
        # Implement Qiniu upload logic here
        # Return the URL of the uploaded image
        pass


class ZhishiXingqiuUploader(BaseUploader):
    def __init__(self):
        self._zsq_api_client = ZsxqApiClient(config.ZSXQ_LOGIN_SUCCESS_COOKEIS)

    def upload(self, file_path: str) -> str:
        """
        Uploads the image to ZhishiXingqiu.
        :param file_path:
        :return:
        """
        image_url = self._zsq_api_client.upload_file(file_path)
        if not image_url:
            raise ValueError(f"Failed to upload image {file_path}")

        return image_url


class ImageUploader:
    def __init__(self, upload_service: str = constant.ALIYUN_UPLOADER):
        """
        Image uploader class that abstracts the upload logic based on the upload service specified.
        :param upload_service:
        """
        if upload_service == constant.ALIYUN_UPLOADER:
            self.uploader = AliyunUploader()
        elif upload_service == constant.QINIU_UPLOADER:
            self.uploader = QiniuUploader()
        elif upload_service == constant.ZHISHIXINGQIU_UPLOADER:
            self.uploader = ZhishiXingqiuUploader()
        else:
            raise ValueError("Invalid upload service")

    def upload(self, file_path: str):
        """
        Uploads the image to the specified service.
        :param file_path:
        :return:
        """
        return self.uploader.upload(file_path)
