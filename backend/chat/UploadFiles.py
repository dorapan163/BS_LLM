import os
import sys
import requests
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logging_config import setup_logger
from backend.chat.config import Config
logger=setup_logger(__name__)
config = Config()


def upload_files(file_paths):
    """
    上传文件到指定接口

    :param file_paths: 要上传的文件路径列表，列表元素为文件路径字符串
    :return: 响应的文本内容，如果请求出错则返回 None
    """
    try:
        # 构建请求 URL
        url = f"{config.api_baseurl}/{config.api_file_upload_endpoint}"

        payload = {}
        files = []
        for file_path in file_paths:
            try:
                file_name = file_path.split('\\')[-1]
                # 推测文件类型
                if file_name.lower().endswith(('.png', '.jpeg', '.jpg', '.webp', '.gif')):
                    file_type = 'image/' + file_name.split('.')[-1]
                else:
                    file_type = 'application/octet-stream'
                files.append(
                    ('file', (file_name, open(file_path, 'rb'), file_type))
                )
            except Exception as e:
                logger.error(f"无法打开文件 {file_path}: {e}")

        headers = {
            'Authorization': f'Bearer {config.appKey["huancat"]}'
        }

        # 发送 POST 请求
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        response.raise_for_status()  # 检查响应状态码
        return response.text
    except requests.RequestException as e:
        logger.error(f"请求出错: {e}")
    except Exception as e:
        logger.error(f"发生未知错误: {e}")
    return None


if __name__ == "__main__":
    file_paths = [
        'C:\\Users\\Administrator\\Pictures\\OIP-C.jpg'
    ]
    result = upload_files(file_paths)
    if result:
        print(result)