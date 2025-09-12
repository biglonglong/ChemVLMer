from openai import OpenAI
from dotenv import load_dotenv
import base64
import json
import os
import re


def encode_image(image_path):
    with open(image_path, "rb") as img_f:
        return base64.b64encode(img_f.read()).decode("utf-8")


# mark
def filter_func(phenomenon, reason):
    if not phenomenon or not reason:
        return False
    return True


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://chat.intern-ai.org.cn/api/v1/",
)

task_with_role = (
    "你是一名精准智能化学实验室的实时审计专家，具备深厚的实验室管理规范知识。"
    "你的任务是对用户提交的实验室场景图像进行严格审计。"
    "请基于图像中的视觉信息合理推断，系统扫描和分析实验场景中的关键元素，识别任何操作规范异常。"
)

# mark
include_dims = """
请囊括以下维度对图像进行分析：
1. 操作程序与逻辑：如机械臂当前动作是否符合标准流程？末端执行器操作是否精确稳定？顺序是否合理？
2. 设备与工具使用：如是否正确选用和操作工具？对工具的操作是否规范？用后归位否？
3. 环境管理与设置：如台面布局是否存在交叉污染、混淆或物理风险？
4. 异常与风险预警：如是否存在仪器读数、容器状态异常？
"""

# mark
filter_dims = """   
"""

img_description = "这是用户提交的实验室场景图像。请基于图像内容进行审计："

output_format = """
- 对无法确认或缺乏视觉证据的内容保持沉默
- 如未发现任何异常，请输出空数组[]
- 每个问题点必须严格按照以下JSON格式描述：

    [
        {
            "phenomenon": "[图像中可见的异常现象]",
            "reason":"[基于视觉信息的合理推断]"
        },
        ...
    ]
"""

img_path = r".\data\test5.jpg"
img_base64 = encode_image(img_path)

chat_rsp = client.chat.completions.create(
    model="intern-latest",
    messages=[
        {"role": "system", "content": task_with_role},
        {"role": "user", "content": include_dims + filter_dims},
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": img_description,
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"},
                },
                # {
                #     "type": "image_url",
                #     "image_url": {
                #         "url": "https://static.openxlab.org.cn/internvl/demo/visionpro.png"  // 支持互联网公开可访问的图片 url 或图片的 base64 编码
                #     }
                # },
                # {
                #     "type": "image_url",                                                     // 单轮对话支持上传多张图片
                #     "image_url": {
                #         "url": "data:image/jpeg;base64,{<encode_image(image_path)>}"           // 替换 <encode_image(image_path)> 为 encoded 后的 base64 格式图片
                #     }
                # }
            ],
        },
        {"role": "user", "content": output_format},
    ],
    stream=False,  # 是否流式返回
)

# # 流式返回
# for chunk in chat_rsp:
#     content_chunk = chunk.choices[0].delta.content
#     if content_chunk is not None:
#         print(content_chunk, end="", flush=True)
# print()

# 非流式返回 + json后处理
for choice in chat_rsp.choices:
    try:
        content_json = json.loads(choice.message.content)
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

        print(json.dumps(pos_content_json, ensure_ascii=False, indent=4))

    except json.JSONDecodeError as e:
        print(choice.message.content)
