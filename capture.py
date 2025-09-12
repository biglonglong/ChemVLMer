import cv2

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("无法打开摄像头")
    exit()


ret, frame = cap.read()
if ret:
    cv2.imshow("Captured Image", frame)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # cv2.imwrite("captured_image.jpg", frame)
    cv2.waitKey(0)
    print("图像已捕获")
else:
    print("无法捕获图像")


# while True:
#     ret, frame = cap.read()
#     if not ret:
#         print("无法捕获图像")
#         break

#     cv2.imshow("Video Stream", frame)
#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break

cap.release()
cv2.destroyAllWindows()
