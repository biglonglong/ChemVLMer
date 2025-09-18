import os
import cv2
from numpy import ndarray

from HKCamera_class import HKCamera

if __name__ == "__main__":
    #  TODO: Change the camera IP as needed
    camera = HKCamera(CameraIp="169.254.128.195")
    # 对摄像头配置进行设置
    try:
        camera.set_Value(
            param_type="enum_value", node_name="PixelFormat", node_value="Mono8"
        )
        camera.set_Value(
            param_type="enum_value", node_name="ExposureAuto", node_value="Continuous"
        )
        # camera.set_Value(
        #     param_type="float_value", node_name="ExposureTime", node_value="400"
        # )
    except Exception as e:
        print(e)
        os._exit(0)
    camera.start_camera()

    while True:
        try:
            # TODO: Change the width as needed
            image: ndarray = camera.get_image(width=448)
            if image is not None:
                cv2.imshow("Captured Image", image)

            key = cv2.waitKey(50) & 0xFF
            if key == ord("e") or key == ord("E"):
                cv2.destroyAllWindows()
                break
        except Exception as e:
            print(e)
