import requests
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logging_config import setup_logger
import backend.konwledgeBase.config as config

logger = setup_logger(__name__)
def create_document_by_file(dataset_id, api_key, file_path):
    """
    Call the API interface to create a document via a file
    :param dataset_id: Dataset ID
    :param api_key: API key
    :param file_path: File path
    :return: API response
    """
    url = f"{config.api_baseurl}/{dataset_id}/document/create-by-file"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "indexing_technique": "high_quality",
        "process_rule": {
            "rules": {
                "pre_processing_rules": [
                    {"id": "remove_extra_spaces", "enabled": True},
                    {"id": "remove_urls_emails", "enabled": True}
                ],
                "segmentation": {
                    "separator": "###",
                    "max_tokens": 500
                }
            },
            "mode": "custom"
        }
    }

    # 将 data 转换为 JSON 字符串，作为表单的一个字段
    data_str = json.dumps(data)
    files = {
        "file": open(file_path, "rb"),
        "data": (None, data_str, "application/json")
    }

    try:
        logger.info(f"开始创建文档，请求 URL: {url}")
        response = requests.post(url, headers=headers, files=files)
        response.raise_for_status()  # Throw an exception if the request fails
        logger.info(f"文档创建成功，响应内容: {response.text}")
        return response.json()
    except requests.RequestException as e:
        logger.error(f"请求出错: {e}")
        if hasattr(response, 'status_code'):
            logger.error(f"状态码: {response.status_code}")
            logger.error(f"响应内容: {response.text}")
        return None
    finally:
        # Properly close the file
        for file in files.values():
            if hasattr(file, 'close'):
                file.close()

# Usage example
if __name__ == "__main__":
    dataset_id = "35892982-37d8-44da-8e4f-0a517f8010ca"
    api_key = "dataset-Dr7zXKIuRbL5077EQUmM0j6f"
    file_path = r"E:\py\BS_LLM\files\sensitive_words.txt"
    logger.info(f"开始调用创建文档函数，数据集 ID: {dataset_id}，文件路径: {file_path}")
    create_document_by_file(dataset_id, api_key, file_path)
