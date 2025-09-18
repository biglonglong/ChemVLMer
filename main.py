import os
import cv2
import json
from numpy import ndarray

from HKCamera_class import HKCamera

from dotenv import load_dotenv
from openai import OpenAI
from utils import (
    encode_image,
    posprocess,
    task_with_role,
    include_dims,
    filter_dims,
    img_description,
    output_format,
)


if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    camera_ip = os.getenv("CameraIp")

    client = OpenAI(
        api_key=api_key,
        base_url="https://chat.intern-ai.org.cn/api/v1/",
    )

    #  TODO: Change the camera IP as needed
    camera = HKCamera(CameraIp=camera_ip)
    try:
        camera.set_Value(
            param_type="enum_value", node_name="PixelFormat", node_value="Mono8"
        )
        camera.set_Value(
            param_type="enum_value", node_name="ExposureAuto", node_value="Continuous"
        )
        camera.start_camera()

        # TODO: Change the width as needed
        image: ndarray = camera.get_image(width=518)
        if image is not None:
            cv2.imshow("Captured Image", image)
            img_path = r".\data\captured_image.jpg"
            cv2.imwrite(img_path, image)
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
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{img_base64}"
                                },
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

            key = cv2.waitKey(0) & 0xFF
            if key == 27:
                cv2.destroyAllWindows()
        else:
            print("Failed to capture image.")

    except Exception as e:
        print(e)
        os._exit(0)
