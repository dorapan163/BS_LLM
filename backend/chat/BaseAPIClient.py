import json
import requests
from typing import Dict, Any, Generator,Union
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logging_config import setup_logger
import ast

# @staticmethod
def unescape_unicode(unicode_str: str) -> str:
    """转义 Unicode 字符串"""
    
    try:
        return ast.literal_eval(f'"{unicode_str}"')
    except SyntaxError:
        return unicode_str
# class BaseAPIClient:
#     def __init__(self, api_url: str, api_key: str):
#         """初始化基类，处理通用配置"""
#         self.api_url = api_url
#         self.api_key = api_key
#         self.headers = {
#             "Authorization": f"Bearer {self.api_key}",
#             "Content-Type": "application/json",
#         }
#         self.logger = setup_logger(self.__class__.__name__)  # 使用类名作为日志器名称
#         self.session = requests.Session()
#         self.session.headers.update(self.headers)
#         self.logger.info(f"初始化 API 客户端，目标 URL: {api_url}")

    # def _send_request(self, method: str, endpoint: str, data: Dict[str, Any] = None, stream: bool = False) -> requests.Response:
    #     """发送通用 HTTP 请求"""
    #     url = f"{self.api_url}/{endpoint}"
    #     try:
    #         response = self.session.request(
    #             method=method,
    #             url=url,
    #             json=data,
    #             stream=stream
    #         )
    #         response.raise_for_status()  # 检查 HTTP 状态码
    #         self.logger.info(f"{method.upper()} 请求成功，状态码: {response.status_code}")
    #         return response
    #     except requests.exceptions.RequestException as e:
    #         self.logger.error(f"请求失败: {e}")
    #         raise  # 抛出异常供子类处理


    # def parse_response(self, response_data: Union[Dict[str, Any], Generator[Dict[str, Any], None, None]]) -> Dict[str, Any]:
    #     pass
    # def close_session(self):
    #     """关闭会话连接"""
    #     self.session.close()
    #     self.logger.info("API 会话已关闭")