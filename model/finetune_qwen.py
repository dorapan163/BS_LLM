import os
import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
    BitsAndBytesConfig,
)
from peft import (
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training,
)

# 配置参数
MODEL_NAME = "D:\\test003\\Qwen3-8B"
DATA_PATH = "D:\\test003\\Choose_data000.jsonl"  # 替换为实际路径
OUTPUT_DIR = "./qwen3-8b-industry-finetuned"
LORA_R = 8
LORA_ALPHA = 32
LORA_DROPOUT = 0.1
LEARNING_RATE = 5e-5
TRAIN_EPOCHS = 3
BATCH_SIZE = 4  # 根据GPU内存调整

def main():
    # 检查GPU可用性
    if not torch.cuda.is_available():
        raise RuntimeError("未检测到GPU，请确保CUDA正确安装并配置。")
    
    # 打印GPU信息
    n_gpus = torch.cuda.device_count()
    device = torch.cuda.current_device()
    print(f"发现 {n_gpus} 个GPU，使用设备: {torch.cuda.get_device_name(device)}")
    
    # 量化配置（使用4-bit量化节省显存）
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
    )
    
    # 加载模型和分词器
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        quantization_config=quantization_config,
        trust_remote_code=True,
        device_map="auto",  # 自动处理设备分配
    )
    
    # 准备LoRA配置
    config = LoraConfig(
        r=LORA_R,
        lora_alpha=LORA_ALPHA,
        target_modules=["q_proj", "v_proj"],  # Qwen3-8B适用的模块
        lora_dropout=LORA_DROPOUT,
        bias="none",
        task_type="CAUSAL_LM",
    )
    
    # 包装模型
    model = prepare_model_for_kbit_training(model)
    model = get_peft_model(model, config)
    
    # 打印可训练参数信息
    model.print_trainable_parameters()
    
    # 加载数据集
    dataset = load_dataset("json", data_files=DATA_PATH)["train"]
    
    # 预处理函数
    def preprocess_function(examples):
        # 构建指令模板
        texts = [
            f"### 问题：{prompt}\n### 回答：{completion}"
            for prompt, completion in zip(examples["prompt"], examples["completion"])
        ]
        
        # 编码文本
        tokenized = tokenizer(texts, padding="max_length", truncation=True, max_length=512)
        
        # 构建标签（用于计算损失）
        tokenized["labels"] = tokenized["input_ids"].copy()
        return tokenized
    
    # 应用预处理
    dataset = dataset.map(preprocess_function, batched=True)
    
    # 设置训练参数
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        learning_rate=LEARNING_RATE,
        per_device_train_batch_size=BATCH_SIZE,
        gradient_accumulation_steps=4,  # 梯度累积，减少内存占用
        num_train_epochs=TRAIN_EPOCHS,
        weight_decay=0.01,
        logging_dir="./logs",
        logging_steps=10,
        save_strategy="steps",
        save_steps=500,
        fp16=True,  # 使用半精度训练
        warmup_ratio=0.05,  # 预热比例
        lr_scheduler_type="cosine",  # 余弦学习率调度
        push_to_hub=False,
    )
    
    # 创建训练器
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        data_collator=DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False),
    )
    
    # 开始训练
    print("开始微调模型...")
    trainer.train()
    
    # 保存微调后的模型
    model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print(f"微调模型已保存至: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()