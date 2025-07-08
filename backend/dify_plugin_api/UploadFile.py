from flask import Flask, request, jsonify
import re
import os
import ahocorasick
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logging_config import setup_logger

app = Flask(__name__)
logger = setup_logger("UplaodFile")  # 使用类名作为日志器名称
# 敏感词文件路径
SENSITIVE_WORDS_FILE = 'files\sensitive_words.txt'

# 初始化 Aho - Corasick 自动机
def build_automaton():
    A = ahocorasick.Automaton()
    if not os.path.exists(SENSITIVE_WORDS_FILE):
        return A
    with open(SENSITIVE_WORDS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            word = line.strip()
            if word:
                A.add_word(word, word)
    A.make_automaton()
    return A

# 初始化敏感词自动机
sensitive_automaton = build_automaton()


@app.route('/api/moderation', methods=['POST'])
def content_moderation():
    """内容审核接口"""
    try:
        # 解析请求体
        data = request.json
        logger.info(f"接收到请求: {data}")
        # 验证请求格式
        if not data or "point" not in data or "params" not in data:
            return jsonify({"error": "Invalid request format"}), 400
        
        params = data["params"]
        # if "app_id" not in params or ("inputs" not in params and "query" not in params):
        #     return jsonify({"error": "Missing required parameters"}), 400
        
        # 提取输入内容
        inputs = params.get("inputs", {})
        query = params.get("query")
    
        # 检查是否包含敏感内容
        flagged = False
        detected_words = set()
        
        # 检查 inputs 中的每个变量
        for var_name, value in inputs.items():
            if isinstance(value, str):
                words = detect_sensitive_words(value.lower())
                if words:
                    flagged = True
                    detected_words.update(words)
        
        # 检查 query
        if isinstance(query, str):
            words = detect_sensitive_words(query.lower())
            if words:
                flagged = True
                detected_words.update(words)
        
        # 构建响应
        if flagged:
            
            # 如果检测到敏感内容
            ret = jsonify({
                "flagged": True,
                "action": "direct_output",
                "preset_response": "检测到敏感内容，请修改后再提交",
                "text": "检测通过"
            })
            logger.info(ret.get_json())
            return ret
        else:
            logger.info("无敏感内容")
            # 如果没有敏感内容，直接通过
            ret = jsonify({
                "flagged": False,
                "action": "direct_output",
                "preset_response": "输出无异常"
                })
            logger.info(ret.get_json())
            return ret
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


def detect_sensitive_words(text):
    """检测文本中的敏感词，返回发现的敏感词集合"""
    detected = set()
    for end_index, original_value in sensitive_automaton.iter(text):
        detected.add(original_value)
    return detected

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)