

import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logging_config import setup_logger
from backend.chat.config import Config

logger = setup_logger(__name__)
config = Config()
# 配置请求参数



def deleteConv():
    try:
        url = f"{config.api_baseurl}/{config.api_conv_endpoint}:conversation_id"
        conversation_id = "f94cb6d0-4504-4b87-966d-8340a4ed90d6"
        url = url.replace(':conversation_id', conversation_id)

        headers = {
            'Authorization': f'Bearer {config.appKey["huancat"]}',
            'Content-Type': 'application/json'
        }

        data = {
            'user': config.default_user
        }
        # 发送 DELETE 请求
        response = requests.delete(url, headers=headers, json=data)

        # 检查响应状态码
        if response.status_code == 200:
            # 打印响应内容
            logger.info("Response data: %s", response.json())
        else:
            # 打印错误信息
            logger.error(
                "Request failed with status code %s: %s",
                response.status_code,
                response.text
            )
    except Exception as e:
        logger.error("An unexpected error occurred: %s", e)


if __name__ == "__main__":
    deleteConv()