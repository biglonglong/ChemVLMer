import base64
import json
import re

# prompts
task_with_role = (
    "你是一名精准智能化学实验室的实时审计专家，具备深厚的实验室管理规范知识。"
    "你的任务是对用户提交的实验室场景图像进行严格审计。"
    "请基于图像中的视觉信息合理推断，系统扫描和分析实验场景中的关键元素，识别任何操作规范异常。"
)

# TODO: Change the include dimensions as needed
include_dims = """
请囊括以下维度对图像进行分析：
1. 操作程序与逻辑：如机械臂当前动作是否符合标准流程？末端执行器操作是否精确稳定？顺序是否合理？
2. 设备与工具使用：如是否正确选用和操作工具？对工具的操作是否规范？用后归位否？
3. 环境管理与设置：如台面布局是否存在交叉污染、混淆或物理风险？
4. 异常与风险预警：如是否存在仪器读数、容器状态异常？
"""

# TODO: Change the filter dimensions as needed
filter_dims = """   
"""

img_description = "这是用户提交的实验室场景图像。请基于图像内容进行审计："

output_format = """
- 对无法确认或缺乏视觉证据的内容保持沉默
- 每个问题点必须严格按照以下JSON格式描述：

    [
        {
            "phenomenon": "[图像中可见的异常现象]",
            "reason":"[基于视觉信息的合理推断]"
        },
        ...
    ]
"""


def posprocess(content):
    match = re.search(r"\[\s*{.*?}\s*\]", content, re.DOTALL)
    if match:
        content_str = match.group(0)
    else:
        raise json.JSONDecodeError("No JSON array found", content, 0)

    content_json = json.loads(content_str)
    pos_content_json = []
    for obj in content_json:
        phenomenon = obj.get("phenomenon", "")
        reason = obj.get("reason", "")
        if filter_func(phenomenon, reason):
            pos_content_json.append(obj)
        else:
            print(
                f'Filtered out invalid entry: "phenomenon": {phenomenon}, "reason": {reason}'
            )

    return pos_content_json


# TODO: Define the filter function based on your criteria
def filter_func(phenomenon, reason):
    if not phenomenon or not reason:
        return False
    return True


def encode_image(image_path):
    with open(image_path, "rb") as img_f:
        return base64.b64encode(img_f.read()).decode("utf-8")
