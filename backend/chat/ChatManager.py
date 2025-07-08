from .agentChat import AgentChat
from .config import Config
from typing import Dict, Optional, List, Union, Any, Generator

class ChatManager:
    def __init__(self):
        """
        初始化 ChatManager 类的实例
        """
        self.config = Config()
        self.chat_clients: Dict[str, AgentChat] = {}
        self.conversation_ids: Dict[str, str] = {}

    def get_chat_client(self, user: str) -> AgentChat:
        """
        获取指定用户的 AgentChat 实例，如果不存在则创建一个新的实例

        :param user: 用户标识
        :return: AgentChat 实例
        """
        if user not in self.chat_clients:
            api_key = self.config.appKey["huancat"]
            self.chat_clients[user] = AgentChat(api_key=api_key)
        return self.chat_clients[user]

    def start_conversation(self, user: str, conversation_id: Optional[str] = None) -> str:
        """
        为指定用户启动一个新的对话

        :param user: 用户标识
        :param conversation_id: 可选的对话 ID，如果未提供则使用空字符串
        :return: 当前对话的 ID
        """
        if conversation_id is None:
            conversation_id = ""
        self.conversation_ids[user] = conversation_id
        return conversation_id

    def converse(
        self,
        user: str,
        query: str,
        files: Optional[List[Dict]] = None,
        response_mode: str = "blocking"
    ) -> Union[Dict[str, Any], Generator[Dict[str, Any], None, None], None]:
        """
        为指定用户发起对话

        :param user: 用户标识
        :param query: 对话的查询内容
        :param files: 包含文件信息的列表，默认为 None
        :param response_mode: 响应模式，可选 "streaming" 或 "blocking"，默认为 "blocking"
        :return: 若为流式响应，返回一个生成器；若为非流式响应，返回解析后的响应数据，如果出现错误则返回 None
        """
        chat_client = self.get_chat_client(user)
        conversation_id = self.conversation_ids.get(user, "")
        return chat_client.converse(
            query=query,
            conversation_id=conversation_id,
            user=user,
            files=files,
            response_mode=response_mode
        )

    def get_conversation_id(self, user: str) -> Optional[str]:
        """
        获取指定用户的当前对话 ID

        :param user: 用户标识
        :return: 当前对话 ID，如果用户没有对话则返回 None
        """
        return self.conversation_ids.get(user)

    def end_conversation(self, user: str) -> None:
        """
        结束指定用户的当前对话

        :param user: 用户标识
        """
        if user in self.conversation_ids:
            del self.conversation_ids[user]