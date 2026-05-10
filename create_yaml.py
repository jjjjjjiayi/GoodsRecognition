import os

# 配置路径
output_dir = r'D:\Project1\yolov5-master\yolov5-master\GoodsRecognition'
data_yaml_path = os.path.join(output_dir, 'data.yaml')

# 类别列表
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
    "ranchA-1", "ranchA-2", "rousongbing", "rusuanjunqishui", "suanlafen",
    "suanlaniurou", "taipingshuda", "tangdaren", "tangdaren2", "tangdaren3",
    "ufo", "ufo2", "wanglaoji", "wanglaoji-c", "wangzainiunai", "weic",
    "weitanai", "weitanai2", "weitanaiditang", "weitaningmeng", "weitaningmeng-bottle",
    "weiweidounai", "wuhounaicha", "wulongcha", "xianglaniurou", "xianguolao",
    "xianxiayuban", "xuebi", "xuebi-b", "xuebi2", "yezhi", "yibao", "yida",
    "yingyangkuaixian", "yitengyuan", "youlemei", "yousuanru", "youyanggudong",
    "yuanqishui", "zaocanmofang", "zihaiguo"
]

# 生成YAML内容
yaml_content = f"""# YOLOv5数据集配置文件
path: D:\\Project1\\yolov5-master\\yolov5-master\\GoodsRecognition\\datasets1
train: images/train
val: images/val

nc: {len(classes)}
names:
"""

# 添加类别名称
for idx, class_name in enumerate(classes):
    yaml_content += f"  {idx}: {class_name}\n"

# 写入文件
with open(data_yaml_path, 'w', encoding='utf-8') as f:
    f.write(yaml_content)

print(f"data.yaml 文件已创建: {data_yaml_path}")
print(f"类别数量: {len(classes)}")