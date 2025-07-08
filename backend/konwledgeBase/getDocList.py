import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logging_config import setup_logger
import backend.konwledgeBase.config as config

logger = setup_logger(__name__)
def get_documents_list(dataset_id, api_key):
    """
    通过 GET 请求获取指定数据集下的文档列表
    :param dataset_id: 数据集 ID
    :param api_key: API 密钥
    :return: API 响应数据，请求失败时返回 None
    """
    url = f"{config.api_baseurl}/{dataset_id}/documents"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    try:
        logger.info(f"开始获取数据集 {dataset_id} 的文档列表，请求 URL: {url}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 若请求失败则抛出异常
        logger.info(f"成功获取数据集 {dataset_id} 的文档列表，响应内容: {response.text}")
        return response.json()
    except requests.RequestException as e:
        logger.error(f"获取数据集 {dataset_id} 的文档列表时请求出错: {e}")
        if hasattr(response, 'status_code'):
            logger.error(f"状态码: {response.status_code}")
            logger.error(f"响应内容: {response.text}")
        return None

# 使用示例
if __name__ == "__main__":
    dataset_id = "35892982-37d8-44da-8e4f-0a517f8010ca"
    document_id = "ec4566b7-a7ef-4e5e-9ef0-212750f78236"
    api_key = "dataset-Dr7zXKIuRbL5077EQUmM0j6f"
    logger.info(f"开始调用获取文档列表函数，数据集 ID: {dataset_id}")
    get_documents_list(dataset_id, api_key)
