import os
import random
import shutil

# 配置参数
val_size = 0.2  # 验证集比例
postfix = 'jpg'
imgpath = r'D:\Project1\yolov5-master\yolov5-master\GoodsRecognition\VOC\JPEGImages'
txtpath = r'D:\Project1\yolov5-master\yolov5-master\GoodsRecognition\VOC\labels'

output_train_img_folder = r'D:\Project1\yolov5-master\yolov5-master\GoodsRecognition\datasets1\images\train'
output_val_img_folder = r'D:\Project1\yolov5-master\yolov5-master\GoodsRecognition\datasets1\images\val'
output_train_txt_folder = r'D:\Project1\yolov5-master\yolov5-master\GoodsRecognition\datasets1\labels\train'
output_val_txt_folder = r'D:\Project1\yolov5-master\yolov5-master\GoodsRecognition\datasets1\labels\val'


def split_dataset():
    # 创建输出目录
    os.makedirs(output_train_img_folder, exist_ok=True)
    os.makedirs(output_val_img_folder, exist_ok=True)
    os.makedirs(output_train_txt_folder, exist_ok=True)
    os.makedirs(output_val_txt_folder, exist_ok=True)

    # 获取所有图片文件名（不含扩展名）
    img_files = [f.replace(f'.{postfix}', '') for f in os.listdir(imgpath)
                 if f.endswith(f'.{postfix}')]

    # 随机打乱并划分
    random.seed(42)  # 固定随机种子，保证可重复性
    random.shuffle(img_files)

    split_idx = int(len(img_files) * (1 - val_size))
    train_files = img_files[:split_idx]
    val_files = img_files[split_idx:]

    # 复制训练集文件
    for name in train_files:
        # 复制图片
        src_img = os.path.join(imgpath, f'{name}.{postfix}')
        dst_img = os.path.join(output_train_img_folder, f'{name}.{postfix}')
        shutil.copy2(src_img, dst_img)

        # 复制标签文件（如果存在）
        src_txt = os.path.join(txtpath, f'{name}.txt')
        dst_txt = os.path.join(output_train_txt_folder, f'{name}.txt')
        if os.path.exists(src_txt):
            shutil.copy2(src_txt, dst_txt)

    # 复制验证集文件
    for name in val_files:
        # 复制图片
        src_img = os.path.join(imgpath, f'{name}.{postfix}')
        dst_img = os.path.join(output_val_img_folder, f'{name}.{postfix}')
        shutil.copy2(src_img, dst_img)

        # 复制标签文件（如果存在）
        src_txt = os.path.join(txtpath, f'{name}.txt')
        dst_txt = os.path.join(output_val_txt_folder, f'{name}.txt')
        if os.path.exists(src_txt):
            shutil.copy2(src_txt, dst_txt)

    print(f"数据集划分完成！")
    print(f"训练集: {len(train_files)} 张图片")
    print(f"验证集: {len(val_files)} 张图片")
    print(f"\n训练集图片目录: {output_train_img_folder}")
    print(f"训练集标签目录: {output_train_txt_folder}")
    print(f"验证集图片目录: {output_val_img_folder}")
    print(f"验证集标签目录: {output_val_txt_folder}")


if __name__ == '__main__':
    split_dataset()