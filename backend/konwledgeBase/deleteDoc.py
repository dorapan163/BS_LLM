import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logging_config import setup_logger
import backend.konwledgeBase.config as config

logger = setup_logger(__name__)
def delete_document(dataset_id, document_id, api_key):
    """
    通过 DELETE 请求删除指定数据集下的文档
    :param dataset_id: 数据集 ID
    :param document_id: 文档 ID
    :param api_key: API 密钥
    :return: API 响应数据，请求失败时返回 None
    """
    url = f"{config.api_baseurl}/{dataset_id}/documents/{document_id}"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    try:
        logger.info(f"开始删除文档，请求 URL: {url}")
        response = requests.delete(url, headers=headers)
        response.raise_for_status()  # 若请求失败则抛出异常
        logger.info(f"文档删除成功，响应内容: {response.text}")
        return response.json()
    except requests.RequestException as e:
        logger.error(f"请求出错: {e}")
        if response.status_code:
            logger.error(f"状态码: {response.status_code}")
            logger.error(f"响应内容: {response.text}")
        return None

# 使用示例
if __name__ == "__main__":
    dataset_id = "35892982-37d8-44da-8e4f-0a517f8010ca"
    document_id = "ec4566b7-a7ef-4e5e-9ef0-212750f78236"
    api_key = "dataset-Dr7zXKIuRbL5077EQUmM0j6f"
    logger.info(f"开始调用删除文档函数，数据集 ID: {dataset_id}，文档 ID: {document_id}")
    delete_document(dataset_id, document_id, api_key)
