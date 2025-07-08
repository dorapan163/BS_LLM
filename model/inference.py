import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# 加载微调后的模型
model_path = "./qwen3-8b-industry-finetuned"
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto"
)

# 生成回答
def generate_answer(question):
    prompt = f"### 问题：{question}\n### 回答："
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=512,
            temperature=0.7,
            top_p=0.9,
            do_sample=True
        )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # 提取回答部分
    answer_start = response.find("### 回答：") + 7
    return response[answer_start:].strip()

# 测试
question = "你们公司招聘岗位有哪些"
answer = generate_answer(question)
print(f"问题: {question}")
print(f"回答: {answer}")