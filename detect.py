from ultralytics import YOLO
import cv2

# 加载训练好的模型
model_path = r'D:\Project1\yolov5-master\yolov5-master\GoodsRecognition\runs\detect\runs\train\exp3\weights\best.pt'
model = YOLO(model_path)

# 图片路径
image_path = r'D:\大三下\人工智能创新实践\ori_000_XYGOC20200313162026456_1.jpg'

# 执行检测
results = model(image_path, conf=0.25, iou=0.45)

# 显示结果
results[0].show()  # 会弹出窗口显示检测结果

# 保存结果
output_path = r'D:\大三下\人工智能创新实践\detection_result.jpg'
results[0].save(output_path)
print(f'检测结果已保存到: {output_path}')

# 打印检测到的物体信息
print("\n检测结果:")
for result in results:
    boxes = result.boxes
    if boxes is not None:
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            conf = box.conf[0].item()
            cls = int(box.cls[0].item())
            name = model.names[cls]
            print(f'  商品: {name}')
            print(f'    置信度: {conf:.2%}')
            print(f'    位置: [{x1:.0f}, {y1:.0f}, {x2:.0f}, {y2:.0f}]')
            print()
    else:
        print("  未检测到任何商品")