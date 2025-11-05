"""
SunnySett Taxonomy Schema - 完整版
定义所有 AI/ML 任务类型、数据类型和应用领域
与 HuggingFace Pipeline 保持一致
"""

# ===== TASKS (任务类型) =====
TASKS = [
    "text-classification",
    "token-classification",
    "question-answering",
    "translation",
    "summarization",
    "text-generation",
    "fill-mask",
    "table-question-answering",
    "image-classification",
    "object-detection",
    "image-segmentation",
    "image-to-text",
    "text-to-image",
    "speech-recognition",
    "audio-classification",
    "text-to-speech",
    "reinforcement-learning",
    "time-series-forecasting",
    "tabular-classification",
    "tabular-regression",
    "agent",
    "document-question-answering",
    "sentence-similarity",
    "zero-shot-classification",
    "optical-character-recognition",
    "pose-detection",
    "depth-estimation",
    "video-classification",
    "semantic-segmentation",
    "super-resolution",
    "image-enhancement",
    "anomaly-detection"
]


# ===== DATA_TYPES (数据类型) =====
DATA_TYPES = {
    "nlp": [
        "text-classification",
        "summarization",
        "question-answering",
        "translation",
        "text-generation",
        "fill-mask",
        "token-classification",
        "sentence-similarity",
        "zero-shot-classification",
        "document-question-answering",
        "table-question-answering"
    ],
    "vision": [
        "image-classification",
        "object-detection",
        "image-segmentation",
        "depth-estimation",
        "pose-detection",
        "super-resolution",
        "semantic-segmentation",
        "image-enhancement",
        "optical-character-recognition"
    ],
    "audio": [
        "speech-recognition",
        "audio-classification",
        "text-to-speech"
    ],
    "multimodal": [
        "image-to-text",
        "text-to-image",
        "video-classification"
    ],
    "tabular": [
        "tabular-regression",
        "tabular-classification",
        "time-series-forecasting"
    ],
    "agentic": [
        "agent",
        "reinforcement-learning",
        "anomaly-detection"
    ]
}


# ===== CATEGORIES (应用领域) =====
CATEGORIES = {
    "finance": [
        "time-series-forecasting",
        "tabular-regression",
        "tabular-classification",
        "text-classification",
        "anomaly-detection"
    ],
    "healthcare": [
        "image-segmentation",
        "image-classification",
        "token-classification",
        "question-answering",
        "anomaly-detection"
    ],
    "engineering": [
        "object-detection",
        "image-segmentation",
        "time-series-forecasting",
        "depth-estimation",
        "pose-detection"
    ],
    "education": [
        "translation",
        "summarization",
        "question-answering",
        "sentence-similarity"
    ],
    "llms": [
        "text-generation",
        "fill-mask",
        "agent",
        "zero-shot-classification"
    ],
    "science": [
        "time-series-forecasting",
        "super-resolution",
        "image-enhancement",
        "anomaly-detection"
    ],
    "geospatial": [
        "image-segmentation",
        "object-detection",
        "depth-estimation"
    ],
    "agriculture": [
        "image-classification",
        "object-detection",
        "time-series-forecasting"
    ],
    "manufacturing": [
        "anomaly-detection",
        "time-series-forecasting",
        "tabular-classification"
    ],
    "energy": [
        "time-series-forecasting",
        "anomaly-detection",
        "reinforcement-learning"
    ],
    "climate": [
        "time-series-forecasting",
        "image-segmentation",
        "super-resolution"
    ],
    "transportation": [
        "object-detection",
        "reinforcement-learning",
        "anomaly-detection"
    ],
    "law": [
        "text-classification",
        "summarization",
        "question-answering"
    ],
    "marketing": [
        "text-classification",
        "summarization",
        "zero-shot-classification"
    ],
    "news": [
        "summarization",
        "text-classification",
        "question-answering"
    ],
    "retail": [
        "tabular-regression",
        "tabular-classification",
        "anomaly-detection"
    ],
    "sports": [
        "time-series-forecasting",
        "video-classification",
        "pose-detection"
    ],
    "art": [
        "text-to-image",
        "image-enhancement"
    ],
    "robotics": [
        "reinforcement-learning",
        "pose-detection",
        "object-detection"
    ],
    "security": [
        "anomaly-detection",
        "audio-classification",
        "object-detection",
        "speech-recognition"
    ],
    "gaming": [
        "reinforcement-learning",
        "agent",
        "text-to-image",
        "text-generation"
    ],
    "multilingual": [
        "translation",
        "zero-shot-classification",
        "summarization"
    ],
    "satellite": [
        "image-segmentation",
        "object-detection",
        "depth-estimation"
    ],
    "chemistry": [
        "tabular-regression",
        "time-series-forecasting",
        "anomaly-detection"
    ],
    "biology": [
        "image-segmentation",
        "anomaly-detection",
        "tabular-regression"
    ],
    "astronomy": [
        "image-segmentation",
        "super-resolution",
        "time-series-forecasting"
    ],
    "psychology": [
        "text-classification",
        "question-answering",
        "speech-recognition"
    ],
    "sociology": [
        "text-classification",
        "summarization",
        "translation"
    ],
    "music": [
        "audio-classification",
        "text-to-speech",
        "speech-recognition"
    ],
    "film": [
        "video-classification",
        "text-to-image",
        "summarization"
    ],
    "fashion": [
        "image-classification",
        "anomaly-detection"
    ],
    "construction": [
        "object-detection",
        "depth-estimation",
        "anomaly-detection"
    ],
    "urban-planning": [
        "image-segmentation",
        "object-detection",
        "super-resolution"
    ],
    "insurance": [
        "tabular-regression",
        "anomaly-detection",
        "text-classification"
    ],
    "real-estate": [
        "tabular-regression",
        "image-classification",
        "summarization"
    ],
    "space": [
        "super-resolution",
        "time-series-forecasting",
        "object-detection"
    ],
    "social-media": [
        "text-classification",
        "agent"
    ],
    "crypto": [
        "time-series-forecasting",
        "anomaly-detection",
        "tabular-regression"
    ],
    "startup": [
        "text-classification",
        "summarization",
        "agent",
        "time-series-forecasting"
    ],
    "ethics": [
        "text-classification",
        "question-answering",
        "agent"
    ],
    "policy": [
        "question-answering",
        "summarization",
        "translation"
    ]
}


# ===== 配置参数 =====
MAX_PER_TASK = 100
SORT = "downloads"
DIRECTION = -1


# ===== 辅助函数 =====

def get_data_type_for_task(task):
    """
    根据任务获取对应的数据类型
    
    参数:
        task: 任务名称，如 "text-generation"
    
    返回:
        str: 数据类型，如 "nlp"，如果找不到返回 None
    
    示例:
        >>> get_data_type_for_task("text-generation")
        'nlp'
        >>> get_data_type_for_task("object-detection")
        'vision'
    """
    for data_type, tasks in DATA_TYPES.items():
        if task in tasks:
            return data_type
    return None


def get_categories_for_task(task):
    """
    根据任务获取所有可能的应用领域
    
    参数:
        task: 任务名称，如 "text-classification"
    
    返回:
        list: 领域列表，如 ["finance", "law", "marketing"]
    
    示例:
        >>> get_categories_for_task("text-generation")
        ['llms', 'gaming']
        >>> get_categories_for_task("object-detection")
        ['engineering', 'agriculture', ...]
    """
    categories = []
    for category, tasks in CATEGORIES.items():
        if task in tasks:
            categories.append(category)
    return categories if categories else ["general"]


def get_all_tasks_for_data_type(data_type):
    """
    获取某个数据类型下的所有任务
    
    参数:
        data_type: 数据类型，如 "nlp"
    
    返回:
        list: 任务列表
    """
    return DATA_TYPES.get(data_type, [])


def get_all_tasks_for_category(category):
    """
    获取某个领域下的所有任务
    
    参数:
        category: 领域名称，如 "finance"
    
    返回:
        list: 任务列表
    """
    return CATEGORIES.get(category, [])


def get_taxonomy_stats():
    """
    获取分类体系的统计信息
    
    返回:
        dict: 包含统计信息的字典
    """
    return {
        "total_tasks": len(TASKS),
        "total_data_types": len(DATA_TYPES),
        "total_categories": len(CATEGORIES),
        "tasks_by_data_type": {
            dt: len(tasks) for dt, tasks in DATA_TYPES.items()
        },
        "tasks_by_category": {
            cat: len(tasks) for cat, tasks in CATEGORIES.items()
        }
    }

