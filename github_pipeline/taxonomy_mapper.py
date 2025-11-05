"""
Taxonomy Mapper - 分类映射器
功能：根据 description, topics, language 推断 task, categories, data_types
"""

import re
from github_pipeline.taxonomy_schema import (
    TASKS,
    DATA_TYPES,
    CATEGORIES,
    get_data_type_for_task,
    get_categories_for_task
)



# ===== 关键词映射 =====
TASK_KEYWORDS = {
    # NLP
    "text-generation": ["gpt", "llm", "language model", "text generation", "generative", "transformer"],
    "text-classification": ["classification", "sentiment", "bert", "roberta"],
    "translation": ["translation", "translate", "multilingual"],
    "summarization": ["summarization", "summary"],
    
    # Vision  
    "object-detection": ["yolo", "detection", "detect", "rcnn", "object detection"],
    "image-segmentation": ["segmentation", "segment", "mask", "sam", "semantic segmentation"],
    "image-classification": ["image classification", "resnet", "vit", "imagenet"],
    
    # 其他
    "reinforcement-learning": ["reinforcement", "rl", "policy"],
}


def find_task_from_text(text):
    """
    从文本中找到最匹配的任务
    
    参数:
        text: 组合的文本（description + topics）
    
    返回:
        str: 任务名称，如 "text-generation"
    """
    text_lower = text.lower()
    
    # 检查每个任务的关键词
    for task, keywords in TASK_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                return task
    
    return "unknown"


def map_taxonomy(model):
    """
    为单个模型添加分类信息
    
    输入格式（GitHub）：
    {
        "modelId": "karpathy/minGPT",
        "description": "...",
        "topics": ["gpt", "pytorch"],
        ...
    }
    
    输出格式（统一）：
    {
        "modelId": "karpathy/minGPT",
        "description": "...",
        "task": "text-generation",          # 新增
        "data_types": ["nlp"],              # 新增
        "categories": ["llms", "education"] # 新增
        ...
    }
    """
    # 组合所有文本信息
    text = " ".join([
        model.get("description", ""),
        model.get("modelId", ""),
        " ".join(model.get("topics", []))
    ])
    
    # 推断任务
    task = find_task_from_text(text)
    
    # 根据任务推断数据类型和领域
    data_type = get_data_type_for_task(task)
    categories = get_categories_for_task(task)
    
    # 添加新字段（保持与 HuggingFace 格式一致）
    model["task"] = task
    model["data_types"] = [data_type] if data_type else []
    model["categories"] = categories
    
    return model


def map_models(models):
    """
    批量处理多个模型
    
    参数:
        models: GitHub loader 输出的模型列表
    
    返回:
        list: 添加了分类信息的模型列表
    """
    print("\n" + "=" * 60)
    print("🧩 Taxonomy Mapper - 开始分类")
    print("=" * 60)
    
    mapped_models = []
    for i, model in enumerate(models, 1):
        print(f"[{i}/{len(models)}] {model['modelId']}")
        
        mapped = map_taxonomy(model)
        
        print(f"  → Task: {mapped['task']}")
        print(f"  → Data Type: {mapped['data_types']}")
        print(f"  → Categories: {', '.join(mapped['categories'][:3])}")  # 只显示前3个
        
        mapped_models.append(mapped)
    
    print("=" * 60)
    print(f"✅ 分类完成！")
    print("=" * 60)
    
    return mapped_models


if __name__ == "__main__":
    import json
    from pathlib import Path

    # 从 github_raw_data.json 读取
    input_path = Path(__file__).resolve().parents[1] / "output/github_raw_data.json"
    with open(input_path, "r", encoding="utf-8") as f:
        models = json.load(f)

    # 执行映射
    mapped = map_models(models)

    # 保存结果
    output_path = Path(__file__).resolve().parents[1] / "output/github_mapped_data.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(mapped, f, indent=2, ensure_ascii=False)

    print(f"✅ category_task_save_to：{output_path}")
