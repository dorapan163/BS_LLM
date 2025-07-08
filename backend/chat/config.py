
class Config:
    _instance = None  # 存储类的唯一实例

    def __new__(cls, *args, **kwargs):
        """
        重写 __new__ 方法以确保只有一个实例被创建

        :return: 类的唯一实例
        """
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.user_conversation_map = {
                "user1": "eac412b6-b9d7-4f9f-bba2-1c11ce499ff9"
            }
            self.api_baseurl = "http://127.0.0.1/v1"
            self.api_chat_endpoint = "chat-messages"
            self.api_conv_endpoint = "conversations"
            self.api_file_upload_endpoint = "files/upload"
            self.appKey = {"huancat": "app-FcKRN6mvSi3TioeEzE7O2Dwz"}
            self.database_url = ""
            self.other_server_params = {}
            self.default_user = "abc-123"
            self.default_response_mode = "blocking"
            self.initialized = True
            self.conv_list_last_id = ""
            self.conv_list_limit = 20

            #logger.info("Config 实例初始化完成")

    # def add_conversation_id(self, username: str, conversation_id: str) -> None:
    #     """添加或更新用户名和会话 ID 的映射"""
    #     self.user_conversation_map[username] = conversation_id

    # def get_conversation_id(self, username: str) -> str:
    #     """根据用户名获取会话 ID"""
    #     return self.user_conversation_map.get(username, "")

    # def remove_conversation_id(self, username: str) -> None:
    #     """删除用户名和会话 ID 的映射"""
    #     if username in self.user_conversation_map:
    #         del self.user_conversation_map[username]

    # def set_api_chaturl(self, api_url: str) -> None:
    #     """设置 API 的 URL"""
    #     self.api_url = api_url

    # def get_api_chaturl(self) -> str:
    #     """获取 API 的 URL"""
    #     return self.api_url

    # def set_api_key(self, api_key: str) -> None:
    #     """设置 API 密钥"""
    #     self.api_key = api_key

    # def get_api_key(self) -> str:
    #     """获取 API 密钥"""
    #     return self.api_key

    # def set_log_level(self, log_level: str) -> None:
    #     """设置日志级别"""
    #     self.log_level = log_level

    # def get_log_level(self) -> str:
    #     """获取日志级别"""
    #     return self.log_level

    # def set_database_url(self, database_url: str) -> None:
    #     """设置数据库连接 URL"""
    #     self.database