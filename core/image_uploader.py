from abc import ABC, abstractmethod
import requests


class BaseUploader(ABC):
    @abstractmethod
    def upload(self, file_path):
        pass


class AliyunUploader(BaseUploader):
    def upload(self, file_path: str):
        # Implement Aliyun upload logic here
        # Return the URL of the uploaded image

        return file_path
        pass


class QiniuUploader(BaseUploader):
    def upload(self, file_path: str):
        # Implement Qiniu upload logic here
        # Return the URL of the uploaded image
        pass


class ImageUploader:
    def __init__(self, upload_service="aliyun"):
        """
        Image uploader class that abstracts the upload logic based on the upload service specified.
        :param upload_service:
        """
        if upload_service == "aliyun":
            self.uploader = AliyunUploader()
        elif upload_service == "qiniu":
            self.uploader = QiniuUploader()
        else:
            raise ValueError("Invalid upload service")

    def upload(self, file_path: str):
        """
        Uploads the image to the specified service.
        :param file_path:
        :return:
        """
        return self.uploader.upload(file_path)
