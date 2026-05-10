import os
import xml.etree.ElementTree as ET

# 路径配置
postfix = 'jpg'
imgpath = r'D:\Project1\yolov5-master\yolov5-master\GoodsRecognition\VOC\JPEGImages'
xmlpath = r'D:\Project1\yolov5-master\yolov5-master\GoodsRecognition\VOC\Annotations'
txtpath = r'D:\Project1\yolov5-master\yolov5-master\GoodsRecognition\VOC\labels'

# 类别列表（按标签顺序，索引从0开始）
classes = [
    "3+2-2", "3jia2", "aerbeisi", "anmuxi", "aoliao", "asamu", "baicha",
    "baishikele", "baishikele-2", "baokuangli", "binghongcha", "bingqilinniunai",
    "bingtangxueli", "buding", "chacui", "chapai", "chapai2", "damaicha",
    "daofandian1", "daofandian2", "daofandian3", "daofandian4", "dongpeng",
    "dongpeng-b", "fenda", "gudasao", "guolicheng", "guolicheng2", "haitai",
    "haochidian", "haoliyou", "heweidao", "heweidao2", "heweidao3", "hongniu",
    "hongniu2", "hongshaoniurou", "jianjiao", "jianlibao", "jindian", "kafei",
    "kaomo_gali", "kaomo_jiaoyan", "kaomo_shaokao", "kaomo_xiangcon", "kebike",
    "kele", "kele-b", "kele-b-2", "laotansuancai", "liaomian", "libaojian",
    "lingdukele", "lingdukele-b", "liziyuan", "lujiaoxiang", "lujikafei",
    "luxiangniurou", "maidong", "mangguoxiaolao", "meiniye", "mengniu",
    "mengniuzaocan", "moliqingcha", "nfc", "niudufen", "niunai", "nongfushanquan",
    "qingdaowangzi-1", "qingdaowangzi-2", "qinningshui", "quchenshixiangcao",
    "rancha-1", "rancha-2", "rousongbing", "rusuanjunqishui", "suanlafen",
    "suanlaniurou", "taipingshuda", "tangdaren", "tangdaren2", "tangdaren3",
    "ufo", "ufo2", "wanglaoji", "wanglaoji-c", "wangzainiunai", "weic",
    "weitanai", "weitanai2", "weitanaiditang", "weitaningmeng", "weitaningmeng-bottle",
    "weiweidounai", "wuhounaicha", "wulongcha", "xianglaniurou", "xianguolao",
    "xianxiayuban", "xuebi", "xuebi-b", "xuebi2", "yezhi", "yibao", "yida",
    "yingyangkuaixian", "yitengyuan", "youlemei", "yousuanru", "youyanggudong",
    "yuanqishui", "zaocanmofang", "zihaiguo"
]

# 创建类别名到索引的映射
class_to_idx = {name: idx for idx, name in enumerate(classes)}


def convert_voc_to_yolo(xml_path, img_width, img_height, txt_path):
    """将单个XML标注转换为YOLO格式的txt文件"""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    with open(txt_path, 'w') as f:
        for obj in root.findall('object'):
            name = obj.find('name').text
            if name not in class_to_idx:
                print(f"警告: 类别 '{name}' 不在预定义列表中，跳过")
                continue

            class_id = class_to_idx[name]
            bndbox = obj.find('bndbox')
            xmin = float(bndbox.find('xmin').text)
            ymin = float(bndbox.find('ymin').text)
            xmax = float(bndbox.find('xmax').text)
            ymax = float(bndbox.find('ymax').text)

            # 转换为YOLO格式（中心点坐标和宽高，归一化）
            x_center = (xmin + xmax) / 2.0 / img_width
            y_center = (ymin + ymax) / 2.0 / img_height
            width = (xmax - xmin) / img_width
            height = (ymax - ymin) / img_height

            f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")


def main():
    # 创建输出目录
    os.makedirs(txtpath, exist_ok=True)

    # 遍历所有XML文件
    for xml_file in os.listdir(xmlpath):
        if not xml_file.endswith('.xml'):
            continue

        xml_path = os.path.join(xmlpath, xml_file)

        # 获取对应的图片尺寸（从同名JPEG图片读取）
        img_name = xml_file.replace('.xml', f'.{postfix}')
        img_path = os.path.join(imgpath, img_name)

        if not os.path.exists(img_path):
            print(f"警告: 图片 {img_path} 不存在，跳过 {xml_file}")
            continue

        # 获取图片尺寸（需要PIL库）
        try:
            from PIL import Image
            with Image.open(img_path) as img:
                img_width, img_height = img.size
        except ImportError:
            print("错误: 需要安装PIL库 (pip install Pillow)")
            return

        # 生成对应的txt文件路径
        txt_name = xml_file.replace('.xml', '.txt')
        txt_path = os.path.join(txtpath, txt_name)

        # 转换并保存
        convert_voc_to_yolo(xml_path, img_width, img_height, txt_path)
        print(f"已转换: {xml_file} -> {txt_name}")


if __name__ == '__main__':
    main()