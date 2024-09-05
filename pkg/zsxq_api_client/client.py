from pathlib import Path
from typing import Dict

from pkg.http_client import SyncHTTPClient
from .help import generate_x_signature, generate_x_request_id
from tenacity import retry, stop_after_attempt, wait_random
import utils


class ZsxqApiClient:
    def __init__(self, login_cookie: str, user_agent: str = None):
        """
        初始化知识星球API客户端。
        :param login_cookie:
        :param user_agent:
        """
        self._base_url = "https://api.zsxq.com"
        self._upload_url = "https://upload-z1.qiniup.com"
        self._login_cookie = login_cookie
        self._x_version = "2.61.0"
        self._user_agent = user_agent or "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"

    def _pre_headers(self, url: str, headers: Dict[str, str] = None) -> Dict[str, str]:
        """
        为请求添加默认headers。
        :param url:
        :param headers:
        :return:
        """
        if headers is None:
            headers = {}
        headers['User-Agent'] = self._user_agent
        headers['Cookie'] = self._login_cookie
        headers['X-Version'] = self._x_version
        headers['X-Request-Id'] = generate_x_request_id()
        headers['X-Timestamp'] = str(utils.get_timestamp())
        headers['X-Signature'] = generate_x_signature(url, headers['X-Timestamp'], headers['X-Request-Id'])
        return headers

    @retry(stop=stop_after_attempt(5), wait=wait_random(1, 3))
    def get_uploads_token(self) -> str:
        """
        获取上传文件前的token。
        :return:
        """
        post_data = {
            'req_data': {
                'type': 'image',
                'usage': 'article',
            }
        }
        with SyncHTTPClient(base_url=self._base_url) as client:
            headers = self._pre_headers('/v2/uploads')
            response = client.post('/v2/uploads', json=post_data, headers=headers)
            if response.status_code == 200 and response.json().get("succeeded"):
                res_data: Dict = response.json()
                return res_data.get("resp_data", {}).get("upload_token")

            raise Exception(f"Failed to get uploads token: {response.text}")

    def upload_file(self, file_path: str) -> str:
        """
        上传文件。
        :param file_path: 文件的绝对路径地址
        :return:
        """
        token = self.get_uploads_token()
        with open(file_path, 'rb') as f:
            files = {"file": (Path(file_path).name, f, "application/octet-stream")}
            data = {"token": token}
            with SyncHTTPClient(base_url=self._upload_url) as client:
                headers = self._pre_headers(self._upload_url)
                response = client.post('', files=files, data=data, headers=headers)
                if response.status_code == 200 and response.json().get("succeeded"):
                    res_data: Dict = response.json()
                    return res_data.get("link", "")

                raise Exception(f"Failed to upload file: {response.text}")
