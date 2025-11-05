"""
Taxonomy Mapper 
function： description, topics, language to get task, categories, data_types
"""

import re
from github_pipeline.taxonomy_schema import (
    TASKS,
    DATA_TYPES,
    CATEGORIES,
    get_data_type_for_task,
    get_categories_for_task
)



# =====  =====
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
  
    """
    text_lower = text.lower()
    
    
    for task, keywords in TASK_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                return task
    
    return "unknown"


def map_taxonomy(model):
  
   
    text = " ".join([
        model.get("description", ""),
        model.get("modelId", ""),
        " ".join(model.get("topics", []))
    ])
    
    # 
    task = find_task_from_text(text)
    
    # 
    data_type = get_data_type_for_task(task)
    categories = get_categories_for_task(task)
    
    # 
    model["task"] = task
    model["data_types"] = [data_type] if data_type else []
    model["categories"] = categories
    
    return model


def map_models(models):

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
    print(f"✅ success！")
    print("=" * 60)
    
    return mapped_models


if __name__ == "__main__":
    import json
    from pathlib import Path

    # from github_raw_data.json to read
    input_path = Path(__file__).resolve().parents[1] / "output/github_raw_data.json"
    with open(input_path, "r", encoding="utf-8") as f:
        models = json.load(f)

    # 
    mapped = map_models(models)

    # 
    output_path = Path(__file__).resolve().parents[1] / "output/github_mapped_data.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(mapped, f, indent=2, ensure_ascii=False)

    print(f"✅ category_task_save_to：{output_path}")
