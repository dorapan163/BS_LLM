
import json
import requests
from typing import List, Dict, Optional, Generator, Union, Any
import os
import sys
import ast
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logging_config import setup_logger
from backend.chat.config import Config
response_type = ["streaming", "blocking"]
config=Config()

def unescape_unicode(unicode_str: str) -> str:
    """转义 Unicode 字符串"""
    
    try:
        return ast.literal_eval(f'"{unicode_str}"')
    except SyntaxError:
        return unicode_str
class AgentChat():
    def __init__(self,  api_key: str) -> None:
        """初始化 AgentChat 类的实例"""
        self.api_url = f"{config.api_baseurl}/{config.api_chat_endpoint}"
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        })
        self.logger = setup_logger(self.__class__.__name__)  # 使用类名作为日志器名称
        self.logger.info(f"初始化 API 客户端，目标 URL: {self.api_url}")
        
    def converse(self,
        query: str,
        conversation_id: str = "",
        user: str = config.default_user,
        files: Optional[List[Dict]] = None,
        response_mode: str = config.default_response_mode,
    ) -> Union[Dict[str, Any], Generator[Dict[str, Any], None, None], None]:
        """
        与代理进行对话。

        :param query: 对话的查询内容。
        :param conversation_id: 会话的 ID，默认为空字符串。
        :param user: 用户标识，默认为 "abc-123"。
        :param files: 包含文件信息的列表，默认为 None。
        :param response_mode: 响应模式，可选 "streaming" 或 "blocking"，默认为 "blocking"。
        :return: 若为流式响应，返回一个生成器；若为非流式响应，返回解析后的响应数据，如果出现错误则返回 None。
        """
        payload = {
            "inputs": {},
            "query": query,
            "response_mode": response_mode,
            "conversation_id": conversation_id,
            "user": user,
            "files": files or [],
        }
        response = self.send_request(payload)
        return response

    def send_request(self, payload: Dict[str, Any]) -> requests.Response:
        try:
            self.logger.info(f"发送请求: {json.dumps(payload, indent=4)}")
            response = self.session.post(
                self.api_url, json=payload, stream=payload["response_mode"] == "streaming"
                )
            response.raise_for_status()  # 检查请求是否成功
            self.logger.info(f"请求成功，状态码: {response.status_code}")

            if payload["response_mode"] == "streaming":
                # 流式响应处理
                return self._process_streaming_response(response)
            else:
                # 阻塞式响应处理
                response_data = self._process_blocking_response(response)
                return response_data

        except requests.exceptions.RequestException as e:
            self.logger.error(f"请求异常: {e}")
            return None
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON解析错误: {e}")
            return None
        except Exception as e:
            self.logger.error(f"未知错误: {e}")
            return None

    def _process_streaming_response(self, response: requests.Response) -> Generator[Dict[str, Any], None, None]:
        """处理流式响应"""
        self.logger.info("开始处理流式响应")
        for line in response.iter_lines():
            if line:
                #self.logger.debug("开始转义")
                #decoded_line = line.decode('utf-8')
                if line.startswith(b'data: '):
                    line = line[len(b'data: '):]
                try:
                    # 解码字节为字符串
                    decoded_line = line.decode('utf-8')
                    # 解析 JSON
                    data = json.loads(decoded_line)
                    # 对需要转义的字符串字段进行 Unicode 转义
                    def unescape_dict(d):
                        if isinstance(d, dict):
                            return {k: unescape_dict(v) for k, v in d.items()}
                        elif isinstance(d, list):
                            return [unescape_dict(item) for item in d]
                        elif isinstance(d, str):
                            return unescape_unicode(d)
                        else:
                            return d
                    data = unescape_dict(data)
                    self.logger.debug(f"收到流式数据块: {json.dumps(data, indent=4)}")
                    yield data
                except json.JSONDecodeError as e:
                    self.logger.error(f"Error decoding JSON chunk: {e}")
                    self.logger.error(f"Chunk: {line}")
    def _process_blocking_response(self, response: requests.Response) -> Dict[str, Any]:
        """处理阻塞式响应"""
        ret=response.json()
        self.logger.info(f"完整响应: {json.dumps(ret, indent=4)}")
        print('hahahahahahahaha!')
        return ret

    def parse_response(self, response_data: Union[Dict[str, Any], Generator[Dict[str, Any], None, None]]) -> Dict[str, Any]:
        """
        解析响应数据，提取并结构化关键信息

        :param response_data: 对话方法返回的响应数据
        :return: 结构化的响应数据
        """
        parsed_result = {
            'event': '',
            'task_id': '',
            'message_id': '',
            'conversation_id': '',
            'answer': '',
            'metadata': {
                'usage': {},
                'retriever_resources': []
            }
        }

        if response_data is None:
            self.logger.warning("无响应数据")
            return parsed_result

        if isinstance(response_data, Generator):
            # 处理流式响应
            self.logger.info("解析流式响应")
            for chunk in response_data:
                parsed_result = self._parse_response_chunk(chunk, parsed_result)
        else:
            # 处理阻塞式响应
            self.logger.info("解析完整响应")
            #logger.debug(f"待解析的完整响应: {json.dumps(response_data, indent=4)}")
            parsed_result = self._parse_response_chunk(response_data, parsed_result)

        self.logger.info(f"解析完成，回答长度: {len(parsed_result['answer'])}")
        return parsed_result
    def _parse_response_chunk(self, chunk: Dict[str, Any], parsed_result: Dict[str, Any]) -> Dict[str, Any]:
            """解析单个响应块"""
            # 提取基本信息
            parsed_result['event'] = chunk.get('event', parsed_result['event'])
            parsed_result['task_id'] = chunk.get('task_id', parsed_result['task_id'])
            parsed_result['message_id'] = chunk.get('message_id', parsed_result['message_id'])
            parsed_result['conversation_id'] = chunk.get('conversation_id', parsed_result['conversation_id'])
            # 提取回答 (处理流式响应时，回答可能会分块返回)
            if 'answer' in chunk:
                answer_length = len(chunk['answer'])
                parsed_result['answer'] += chunk['answer']
                self.logger.debug(f"追加回答内容，长度: {answer_length}")
            
            # 提取元数据
            if 'metadata' in chunk:
                metadata = chunk['metadata']
                
                # 提取使用信息
                if 'usage' in metadata:
                    parsed_result['metadata']['usage'].update(metadata['usage'])
                    self.logger.debug("更新使用信息")
                
                # 提取检索资源
                if 'retriever_resources' in metadata:
                    resources_count = len(metadata['retriever_resources'])
                    parsed_result['metadata']['retriever_resources'].extend(metadata['retriever_resources'])
                    self.logger.debug(f"添加检索资源，数量: {resources_count}")
            
            return parsed_result
if __name__ == "__main__":
    cfg=Config()
    # 初始化客户端                  http://192.168.1.13/v1/chat-messages  app-X9qCCFA0wR1fJrQ6VtVyH4rY
    client = AgentChat(api_key=cfg.appKey["huancat"])

    # 获取完整响应并解析
    #task_id=9883db5b-6c09-4f1b-8c78-568e195dc5a6
    #conversation_id=f3f652a6-ce47-459f-9fb1-1a246aff777f
    full_response = client.converse(query="你好", conversation_id="f3f652a6-ce47-459f-9fb1-1a246aff777f", user="abc-123",response_mode=response_type[1])
    parsed_data = client.parse_response(full_response)

    # 打印关键信息  
    print(f"任务ID: {parsed_data['task_id']}")
    print(f"对话ID: {parsed_data['conversation_id']}")
    print(f"回答内容: {parsed_data['answer']}")

    # 打印使用信息
    usage = parsed_data['metadata']['usage']
    print(f"提示词token数: {usage.get('prompt_tokens')}")
    print(f"回复token数: {usage.get('completion_tokens')}")
    print(f"总费用: {usage.get('total_price')} {usage.get('currency')}")

    # 打印检索资源
    resources = parsed_data['metadata']['retriever_resources']
    for i, resource in enumerate(resources, 1):
        print(f"\n检索资源 {i}:")
        print(f"  数据集: {resource.get('dataset_name')}")
        print(f"  文档: {resource.get('document_name')}")
        print(f"  内容片段: {resource.get('content')[:100]}...")        