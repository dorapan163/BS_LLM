### Flask 应用 API 文档

下面是 Flask 应用的详细 API 文档，该应用提供了对话管理、文件上传和代理交互等功能。

### 基础信息

- **服务器地址**：默认运行在 `http://localhost:5000`
- **所有接口返回格式**：JSON 格式
- **错误响应格式**：
  ```json
  {
    "message": "错误描述",
    "error": "具体错误信息"
  }
  ```

### 接口详情

#### 1. 获取对话列表

```
GET /get_conversation_list
```

**功能**：获取所有对话的列表。

**返回值**：

- **成功**（状态码 200）：对话列表数据。
- **失败**（状态码 500）：
  ```json
  {
    "message": "获取对话列表失败"
  }
  ```

#### 2. 删除对话

```
DELETE /delete_conv
```

**功能**：删除指定对话。

**返回值**：

- **成功**（状态码 200）：
  ```json
  {
    "message": "对话删除成功"
  }
  ```
- **失败**（状态码 500）：
  ```json
  {
    "message": "对话删除失败",
    "error": "具体错误信息"
  }
  ```

#### 3. 上传文件

```
POST /upload_files
```

**功能**：上传文件路径列表。

**请求参数**：

```json
{
  "file_paths": ["path/to/file1", "path/to/file2"]
}
```

**返回值**：

- **成功**（状态码 200）：
  ```json
  {
    "message": "文件上传成功",
    "response": "上传结果信息"
  }
  ```
- **失败**（状态码 500）：
  ```json
  {
    "message": "文件上传失败"
  }
  ```
- **参数错误**（状态码 400）：
  ```json
  {
    "message": "请提供有效的文件路径列表"
  }
  ```

#### 4. 与代理对话

```
POST /converse
```

**功能**：与代理进行交互，支持流式响应。

示例

```
curl -X POST http://127.0.0.1:5000/converse \
-H "Content-Type: application/json" \
-d '{
    "user_id": "user123",
    "conversation_id": "conv456",
    "manager_id": "manager789",
    "query": "你好",
    "files": ["file1.txt", "file2.txt"],
    "response_mode": "blocking"
}'
```

**请求参数**：

```json
{
  "query": "用户查询内容",
  "user": "用户名",
  "files": ["file1", "file2"],
  "response_mode": "响应模式",
  "conversation_id": "对话ID"
}
```

**参数说明**：

- `query`（必填）：用户的查询内容。
- `user`（可选）：用户名，默认值来自配置。
- `files`（可选）：文件列表。
- `response_mode`（可选）：响应模式，默认值来自配置。
- `conversation_id`（可选）：对话ID，若未提供则尝试获取当前用户的对话ID，没有则创建新对话。

**返回值**：

- **成功（非流式）**（状态码 200）：
  ```json
  {
    "解析后的响应内容"
  }
  ```
- **成功（流式）**（状态码 200）：
  ```json
  {"解析后的响应块1"}
  {"解析后的响应块2"}
  ...
  ```
- **失败**（状态码 500）：
  ```json
  {
    "message": "对话请求出错",
    "error": "具体错误信息"
  }
  ```
- **参数错误**（状态码 400）：
  ```json
  {
    "message": "请提供查询内容"
  }
  ```

### 错误码说明

| 状态码 | 含义           |
| ------ | -------------- |
| 200    | 请求成功       |
| 400    | 参数错误       |
| 500    | 服务器内部错误 |

### 注意事项

- 对于 `/converse` 接口，若未提供 `conversation_id`，系统会自动创建新对话。
- 流式响应会逐块返回数据，客户端需要按行解析。
- 所有接口都以 JSON 格式进行数据交互。





update 获取客户端数量和具体信息

将vedio换成canvas显示视频流
