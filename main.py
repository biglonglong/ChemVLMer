from openai import OpenAI  # openAI Python SDK
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://chat.intern-ai.org.cn/api/v1/",
)

chat_rsp = client.chat.completions.create(
    model="intern-latest",
    messages=[
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "你好，我是 internvl"},
        {
            "role": "user",
            "content": [  # 用户的图文提问内容，数组形式
                {
                    "type": "text",  # type 支持 text/image_url
                    "text": "Describe the image please",
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://static.openxlab.org.cn/internvl/demo/visionpro.png"  # 支持互联网公开可访问的图片 url 或图片的 base64 编码
                    },
                },
                {
                    "type": "image_url",  # 单轮对话支持上传多张图片
                    "image_url": {
                        "url": "data:image/jpeg;base64,{<encode_image(image_path)>}"  # 替换 <encode_image(image_path)> 为 encoded 后的 base64 格式图片
                    },
                },
            ],
        },
    ],
    stream=True,  # 是否流式返回
)

# 流式返回
for chunk in chat_rsp:
    content_chunk = chunk.choices[0].delta.content
    if content_chunk is not None:
        print(content_chunk, end="", flush=True)
print()

# # 非流式返回
# for choice in chat_rsp.choices:
#     print(choice.message.content)