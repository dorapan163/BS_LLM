import requests
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logging_config import setup_logger
import backend.konwledgeBase.config as config

logger = setup_logger(__name__)
def update_document_by_file(dataset_id, document_id, api_key, file_path):
    """
    通过文件更新指定数据集下的文档
    :param dataset_id: 数据集 ID
    :param document_id: 文档 ID
    :param api_key: API 密钥
    :param file_path: 文件路径
    :return: API 响应数据，请求失败时返回 None
    """
    url = f"{config.api_baseurl}/{dataset_id}/documents/{document_id}/update-by-file"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "name": "Dify",
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
        logger.info(f"开始更新数据集 {dataset_id} 中文档 {document_id}，请求 URL: {url}")
        response = requests.post(url, headers=headers, files=files)
        response.raise_for_status()  # 若请求失败则抛出异常
        ret = response.json()
        logger.info(f"成功更新数据集 {dataset_id} 中文档 {document_id}，文档信息: {ret['document']}")
        return ret
    except requests.RequestException as e:
        logger.error(f"更新数据集 {dataset_id} 中文档 {document_id} 时请求出错: {e}")
        if hasattr(response, 'status_code'):
            logger.error(f"状态码: {response.status_code}")
            logger.error(f"响应内容: {response.text}")
        return None
    finally:
        # 正确关闭文件
        for file in files.values():
            if hasattr(file, 'close'):
                file.close()

# 使用示例
if __name__ == "__main__":
    dataset_id = "35892982-37d8-44da-8e4f-0a517f8010ca"
    api_key = "dataset-Dr7zXKIuRbL5077EQUmM0j6f"
    document_id = "5cb932e1-0bbe-4f56-8925-b06ab0363706"
    file_path = r"E:\py\BS_LLM\files\sensitive_words.txt"
    logger.info(f"开始调用更新文档函数，数据集 ID: {dataset_id}，文档 ID: {document_id}，文件路径: {file_path}")
    update_document_by_file(dataset_id, document_id, api_key, file_path)