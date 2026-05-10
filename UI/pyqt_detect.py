import sys
import json
from pathlib import Path
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ultralytics import YOLO

sys.path.append(str(Path(__file__).resolve().parent.parent))
from database.db_manager import init_db, GoodsManager, OrdersManager, analyze_images, CLASS_NAMES_CN


class GoodsTab(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.initUI()
        self.load_goods()

    def initUI(self):
        layout = QVBoxLayout()

        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton('添加商品')
        self.btn_edit = QPushButton('编辑商品')
        self.btn_delete = QPushButton('删除商品')
        self.btn_update_stock = QPushButton('图片识别更新库存')
        self.btn_refresh = QPushButton('刷新')

        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_update_stock)
        btn_layout.addWidget(self.btn_refresh)
        btn_layout.addStretch()

        self.btn_add.clicked.connect(self.add_goods)
        self.btn_edit.clicked.connect(self.edit_goods)
        self.btn_delete.clicked.connect(self.delete_goods)
        self.btn_update_stock.clicked.connect(self.update_stock_by_image)
        self.btn_refresh.clicked.connect(self.load_goods)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['ID', '商品名', 'Label', '价格', '库存', '状态'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        layout.addLayout(btn_layout)
        layout.addWidget(self.table)
        self.setLayout(layout)

    def load_goods(self):
        goods_list = GoodsManager.get_all()
        self.table.setRowCount(len(goods_list))
        for i, g in enumerate(goods_list):
            self.table.setItem(i, 0, QTableWidgetItem(g['id']))
            self.table.setItem(i, 1, QTableWidgetItem(g['name']))
            self.table.setItem(i, 2, QTableWidgetItem(str(g['label'])))
            self.table.setItem(i, 3, QTableWidgetItem(str(g['price'])))
            self.table.setItem(i, 4, QTableWidgetItem(str(g['stock'])))
            self.table.setItem(i, 5, QTableWidgetItem('正常'))

    def add_goods(self):
        dialog = GoodsDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            name, label, price = dialog.get_data()
            GoodsManager.add(name, label, price)
            self.load_goods()

    def edit_goods(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, '提示', '请选择要编辑的商品')
            return
        gid = self.table.item(row, 0).text()
        name = self.table.item(row, 1).text()
        label = self.table.item(row, 2).text()
        price = float(self.table.item(row, 3).text())

        dialog = GoodsDialog(self, name, label, price)
        if dialog.exec_() == QDialog.Accepted:
            name, label, price = dialog.get_data()
            GoodsManager.update(gid, name, label, price)
            self.load_goods()

    def delete_goods(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, '提示', '请选择要删除的商品')
            return
        reply = QMessageBox.question(self, '确认', '确定删除该商品？', QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            gid = self.table.item(row, 0).text()
            GoodsManager.delete(gid)
            self.load_goods()

    def update_stock_by_image(self):
        fname, _ = QFileDialog.getOpenFileName(self, '选择图片', '.', '图像文件(*.jpg *.png *.jpeg)')
        if not fname:
            return

        results = self.model(fname, conf=0.5, iou=0.6)
        boxes = results[0].boxes
        if boxes is None:
            QMessageBox.information(self, '提示', '未检测到商品')
            return

        counts = {}
        for box in boxes:
            cls = int(box.cls[0].item())
            counts[cls] = counts.get(cls, 0) + 1

        for label, count in counts.items():
            GoodsManager.update_stock(label, count)

        self.load_goods()
        QMessageBox.information(self, '成功', f'库存已更新，识别到{len(counts)}种商品')


class GoodsDialog(QDialog):
    def __init__(self, parent=None, name='', label='', price=0):
        super().__init__(parent)
        self.setWindowTitle('商品信息')
        layout = QFormLayout()

        self.name_edit = QLineEdit(name)
        self.label_edit = QLineEdit(label)
        self.price_edit = QDoubleSpinBox()
        self.price_edit.setRange(0, 9999)
        self.price_edit.setValue(price)
        self.price_edit.setSingleStep(0.5)

        layout.addRow('商品名:', self.name_edit)
        layout.addRow('Label:', self.label_edit)
        layout.addRow('价格:', self.price_edit)

        btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        layout.addRow(btn_box)

        self.setLayout(layout)

    def get_data(self):
        return self.name_edit.text(), self.label_edit.text(), self.price_edit.value()


class OrdersTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_orders()

    def initUI(self):
        layout = QVBoxLayout()

        btn_layout = QHBoxLayout()
        self.btn_refresh = QPushButton('刷新')
        self.btn_detail = QPushButton('查看详情')
        btn_layout.addWidget(self.btn_refresh)
        btn_layout.addWidget(self.btn_detail)
        btn_layout.addStretch()

        self.btn_refresh.clicked.connect(self.load_orders)
        self.btn_detail.clicked.connect(self.show_detail)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['订单ID', '订单时间', '商品种数', '总金额', '状态'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        layout.addLayout(btn_layout)
        layout.addWidget(self.table)
        self.setLayout(layout)

    def load_orders(self):
        orders = OrdersManager.get_all()
        self.table.setRowCount(len(orders))
        for i, o in enumerate(orders):
            goods = json.loads(o['goods_info']) if o['goods_info'] else []
            status_map = {'Pending': '待处理', 'Completed': '已完成', 'Cancelled': '已取消'}
            self.table.setItem(i, 0, QTableWidgetItem(o['id']))
            self.table.setItem(i, 1, QTableWidgetItem(o['order_time']))
            self.table.setItem(i, 2, QTableWidgetItem(str(len(goods))))
            self.table.setItem(i, 3, QTableWidgetItem(f"{o['total_price']:.2f}"))
            self.table.setItem(i, 4, QTableWidgetItem(status_map.get(o['status'], o['status'])))

    def show_detail(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, '提示', '请选择订单')
            return
        oid = self.table.item(row, 0).text()
        detail = OrdersManager.get_detail(oid)
        if not detail:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle('订单详情')
        layout = QVBoxLayout()

        info_text = f"订单ID: {detail['id']}\n"
        info_text += f"订单时间: {detail['order_time']}\n"
        info_text += f"订单状态: {detail['status']}\n"
        info_text += f"总金额: {detail['total_price']:.2f}\n\n"
        info_text += "商品明细:\n"

        goods = detail['goods_info']
        if goods:
            for g in goods:
                info_text += f"  {g['name']} x{g['quantity']} - ¥{g['price']} (小计: ¥{g['subtotal']:.2f})\n"
        else:
            info_text += "  无商品\n"

        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setPlainText(info_text)
        layout.addWidget(text_edit)

        btn = QPushButton('关闭')
        btn.clicked.connect(dialog.close)
        layout.addWidget(btn)

        dialog.setLayout(layout)
        dialog.resize(500, 400)
        dialog.exec_()


class SmartCartTab(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.before_img = None
        self.after_img = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        img_layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        self.btn_before = QPushButton('选择开门前图片')
        self.label_before = QLabel('开门前图片')
        self.label_before.setAlignment(Qt.AlignCenter)
        self.label_before.setMinimumSize(300, 200)
        self.label_before.setStyleSheet('border: 1px solid gray;')
        self.btn_before.clicked.connect(self.select_before)
        left_layout.addWidget(self.btn_before)
        left_layout.addWidget(self.label_before)

        right_layout = QVBoxLayout()
        self.btn_after = QPushButton('选择关门后图片')
        self.label_after = QLabel('关门后图片')
        self.label_after.setAlignment(Qt.AlignCenter)
        self.label_after.setMinimumSize(300, 200)
        self.label_after.setStyleSheet('border: 1px solid gray;')
        self.btn_after.clicked.connect(self.select_after)
        right_layout.addWidget(self.btn_after)
        right_layout.addWidget(self.label_after)

        img_layout.addLayout(left_layout)
        img_layout.addLayout(right_layout)

        self.btn_analyze = QPushButton('分析')
        self.btn_analyze.clicked.connect(self.analyze)

        self.btn_create_order = QPushButton('创建订单')
        self.btn_create_order.setEnabled(False)
        self.btn_create_order.clicked.connect(self.create_order)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_analyze)
        btn_layout.addWidget(self.btn_create_order)
        btn_layout.addStretch()

        layout.addLayout(img_layout)
        layout.addLayout(btn_layout)
        layout.addWidget(self.result_text)
        self.setLayout(layout)

        self.purchased = []
        self.total = 0
        self.status = ''

    def select_before(self):
        fname, _ = QFileDialog.getOpenFileName(self, '选择开门前图片', '.', '图像文件(*.jpg *.png *.jpeg)')
        if fname:
            self.before_img = fname
            self.show_image(self.label_before, fname)

    def select_after(self):
        fname, _ = QFileDialog.getOpenFileName(self, '选择关门后图片', '.', '图像文件(*.jpg *.png *.jpeg)')
        if fname:
            self.after_img = fname
            self.show_image(self.label_after, fname)

    def show_image(self, label, path):
        pixmap = QPixmap(path)
        scaled = pixmap.scaled(300, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label.setPixmap(scaled)

    def analyze(self):
        if not self.before_img or not self.after_img:
            QMessageBox.warning(self, '提示', '请先选择两张图片')
            return

        self.purchased, self.total, self.status, before_counts, after_counts = analyze_images(
            self.before_img, self.after_img, self.model
        )

        result = f"开门前检测: {before_counts}\n"
        result += f"关门后检测: {after_counts}\n\n"

        if self.status == 'Cancelled':
            result += "结果: 商品无变化，订单已取消\n"
        else:
            result += f"状态: {self.status}\n"
            result += "购买商品:\n"
            for p in self.purchased:
                result += f"  {p['name']} x{p['quantity']} - ¥{p['price']} (小计: ¥{p['subtotal']:.2f})\n"
            result += f"\n总金额: ¥{self.total:.2f}\n"

        self.result_text.setPlainText(result)
        self.btn_create_order.setEnabled(self.status == 'Completed')

    def create_order(self):
        if not self.purchased:
            return
        oid = OrdersManager.create(self.purchased, self.total, self.status)
        QMessageBox.information(self, '成功', f'订单已创建\n订单ID: {oid}')
        self.btn_create_order.setEnabled(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    init_db()

    weights_path = r'D:\Project1\yolov5-master\yolov5-master\GoodsRecognition\runs\detect\runs\train\exp3\weights\best.pt'
    model = YOLO(weights_path)

    tab_widget = QTabWidget()
    tab_widget.addTab(GoodsTab(model), '商品管理')
    tab_widget.addTab(OrdersTab(), '订单管理')
    tab_widget.addTab(SmartCartTab(model), '智能购物车')

    tab_widget.setWindowTitle('商品识别系统')
    tab_widget.resize(900, 600)
    tab_widget.show()

    sys.exit(app.exec_())
