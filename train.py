import warnings

warnings.filterwarnings('ignore')

from ultralytics import YOLO

if __name__ == '__main__':
    # 使用GPU训练（自动检测可用GPU）
    model = YOLO(r'D:\Project1\yolov5-master\yolov5-master\GoodsRecognition\yolov5su.pt')

    model.train(
        data=r'D:\Project1\yolov5-master\yolov5-master\GoodsRecognition\data.yaml',
        imgsz=640,
        epochs=10,
        batch=4,
        workers=0,  # Windows下建议设为0避免多进程问题
        device=0,  # 使用GPU0（如果有多个GPU，可以设为'0,1'）
        optimizer='SGD',
        close_mosaic=10,
        resume=False,
        project='runs/train',
        name='exp',
        single_cls=False,
        cache=False,
    )