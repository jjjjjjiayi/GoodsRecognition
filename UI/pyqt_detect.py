import sys
import cv2
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ultralytics import YOLO


class Qdetection1(QWidget):
    def __init__(self, model):
        super(Qdetection1, self).__init__()
        self.model = model
        self.initUI()

    def initUI(self):
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)

        # 添加参数控制
        control_widget = QWidget()
        control_layout = QHBoxLayout(control_widget)

        self.label_conf = QLabel('置信度阈值:')
        self.spin_conf = QDoubleSpinBox()
        self.spin_conf.setRange(0.1, 0.9)
        self.spin_conf.setValue(0.5)
        self.spin_conf.setSingleStep(0.05)

        self.label_iou = QLabel('IoU阈值:')
        self.spin_iou = QDoubleSpinBox()
        self.spin_iou.setRange(0.3, 0.9)
        self.spin_iou.setValue(0.6)
        self.spin_iou.setSingleStep(0.05)

        control_layout.addWidget(self.label_conf)
        control_layout.addWidget(self.spin_conf)
        control_layout.addWidget(self.label_iou)
        control_layout.addWidget(self.spin_iou)
        control_layout.addStretch()

        self.button1 = QPushButton('上传图片')
        self.button1.clicked.connect(self.loadImage)
        control_layout.addWidget(self.button1)

        self.main_layout.addWidget(control_widget, 0, 0, 1, 2)

        self.imageLabel1 = QLabel()
        self.imageLabel1.setText("原始图片")
        self.imageLabel1.setAlignment(Qt.AlignCenter)
        self.imageLabel1.setMinimumSize(400, 300)

        self.imageLabel2 = QLabel()
        self.imageLabel2.setText("检测结果")
        self.imageLabel2.setAlignment(Qt.AlignCenter)
        self.imageLabel2.setMinimumSize(400, 300)

        self.main_layout.addWidget(self.imageLabel1, 1, 0, 1, 1)
        self.main_layout.addWidget(self.imageLabel2, 1, 1, 1, 1)

    def loadImage(self):
        fname, _ = QFileDialog.getOpenFileName(self, '打开文件', '.', '图像文件(*.jpg *.png *.jpeg)')
        if not fname:
            print("未选择图片")
            return

        img = cv2.imread(fname)
        if img is None:
            print("无法读取图片")
            return

        # 获取用户设置的阈值
        conf_thres = self.spin_conf.value()
        iou_thres = self.spin_iou.value()

        print(f"\n使用参数: 置信度={conf_thres}, IoU={iou_thres}")

        # 执行检测
        results = self.model(fname, conf=conf_thres, iou=iou_thres)
        result_img = results[0].plot()

        # 显示检测信息
        boxes = results[0].boxes
        if boxes is not None:
            print(f"检测到 {len(boxes)} 个商品:")
            for box in boxes:
                conf = box.conf[0].item()
                cls = int(box.cls[0].item())
                name = self.model.names[cls]
                print(f"  - {name}: {conf:.2%}")
        else:
            print("未检测到商品")

        # 转换并显示图片
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result_img_rgb = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)

        img_rgb = self.resize_image(img_rgb, 400, 300)
        result_img_rgb = self.resize_image(result_img_rgb, 400, 300)

        # 显示原始图片
        h, w, ch = img_rgb.shape
        bytes_per_line = ch * w
        qimg = QImage(img_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.imageLabel1.setPixmap(QPixmap.fromImage(qimg))

        # 显示检测结果
        h, w, ch = result_img_rgb.shape
        bytes_per_line = ch * w
        qimg_result = QImage(result_img_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.imageLabel2.setPixmap(QPixmap.fromImage(qimg_result))

    def resize_image(self, img, max_width, max_height):
        height, width = img.shape[:2]
        ratio = min(max_width / width, max_height / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        resized = cv2.resize(img, (new_width, new_height))
        return resized


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    # 加载模型
    weights_path = r'D:\Project1\yolov5-master\yolov5-master\GoodsRecognition\runs\detect\runs\train\exp3\weights\best.pt'
    model = YOLO(weights_path)

    # 创建标签页
    my_tabwidget = QTabWidget()
    tab1_widget = Qdetection1(model)
    my_tabwidget.setWindowTitle('目标检测演示')
    my_tabwidget.addTab(tab1_widget, '图片检测')
    my_tabwidget.resize(900, 600)
    my_tabwidget.show()

    sys.exit(app.exec_())