import requests

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logging_config import setup_logger
from backend.chat.config import Config
logger=setup_logger(__name__)
config = Config()


def get_conversation_list():
    """
    获取对话列表并处理响应。

    :return: 若请求成功，返回响应数据中的 "data" 部分；若失败，返回 None
    """
    try:
        # 配置请求参数
        url = f"{config.api_baseurl}/{config.api_conv_endpoint}"
        params = {
            'user': config.default_user,
            'last_id': config.conv_list_last_id,
            'limit': config.conv_list_limit
        }
        headers = {
            'Authorization': f'Bearer {config.appKey["huancat"]}'
        }

        # 发送 GET 请求
        response = requests.get(url, params=params, headers=headers)
        response_data = response.json()

        # 检查响应状态码
        if response.status_code == 200:
            # 打印响应内容
            logger.info("Response data: %s", response_data["data"])
            return response_data["data"]
        else:
            # 打印错误信息
            logger.error("Request failed with status code %s: %s", response.status_code, response.text)
    except requests.RequestException as e:
        logger.error("Request error occurred: %s", e)
    except ValueError as e:
        logger.error("Failed to decode JSON response: %s", e)
    return None


if __name__ == "__main__":
    get_conversation_list()


# def parse_conversation_list_response(response_json):
#     """
#     解析对话列表响应的 JSON 数据。

#     :param response_json: 响应的 JSON 数据
#     :return: 包含解析后数据的字典
#     """
#     parsed_data = {
#         'limit': response_json.get('limit'),
#         'has_more': response_json.get('has_more'),
#         'conversations': []
#     }
    
#     for conversation in response_json.get('data', []):
#         parsed_conversation = {
#             'id': conversation.get('id'),
#             'name': conversation.get('name'),
#             'inputs': conversation.get('inputs'),
#             'status': conversation.get('status'),
#             'introduction': conversation.get('introduction'),
#             'created_at': conversation.get('created_at'),
#             'updated_at': conversation.get('updated_at')
#         }
#         parsed_data['conversations'].append(parsed_conversation)
    
#     return parsed_data