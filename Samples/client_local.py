from openai import OpenAI
from dotenv import load_dotenv
from utils import (
    encode_image,
    posprocess,
    task_with_role,
    include_dims,
    filter_dims,
    img_description,
    output_format,
)
import json
import os


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://chat.intern-ai.org.cn/api/v1/",
)


img_path = r".\data\test.jpg"
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
            ],
        },
        {"role": "user", "content": output_format},
    ],
    stream=False,
)

for choice in chat_rsp.choices:
    try:
        pos_content_json = posprocess(choice.message.content)
        print(json.dumps(pos_content_json, ensure_ascii=False, indent=4))
    except json.JSONDecodeError as e:
        print(choice.message.content)
