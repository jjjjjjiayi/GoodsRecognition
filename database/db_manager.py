import sqlite3
import json
import uuid
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "goods.db"

CLASS_MAPPING = {
    0: '3+2-2', 1: '3jia2', 2: 'aerbisi', 3: 'anmuxi', 4: 'aoliao',
    5: 'asamu', 6: 'baicha', 7: 'baishikele', 8: 'baishikele-2', 9: 'baokuangli',
    10: 'binghongcha', 11: 'bingqilinniunai', 12: 'bingtangxueli', 13: 'buding',
    14: 'chacui', 15: 'chapai', 16: 'chapai2', 17: 'damaicha', 18: 'daofandian1',
    19: 'daofandian2', 20: 'daofandian3', 21: 'daofandian4', 22: 'dongpeng',
    23: 'dongpeng-b', 24: 'fenda', 25: 'gudasao', 26: 'guolicheng', 27: 'guolicheng2',
    28: 'haitai', 29: 'haochidian', 30: 'haoliyou', 31: 'heweidao', 32: 'heweidao2',
    33: 'heweidao3', 34: 'hongniu', 35: 'hongniu2', 36: 'hongshaoniurou', 37: 'jianjiao',
    38: 'jianlibao', 39: 'jindian', 40: 'kafei', 41: 'kaomo_gali', 42: 'kaomo_jiaoyan',
    43: 'kaomo_shaokao', 44: 'kaomo_xiangcon', 45: 'kebike', 46: 'kele', 47: 'kele-b',
    48: 'kele-b-2', 49: 'laotansuancai', 50: 'liaomian', 51: 'libaojian', 52: 'lingdukele',
    53: 'lingdukele-b', 54: 'liziyuan', 55: 'lujiaoxiang', 56: 'lujikafei', 57: 'luxiangniurou',
    58: 'maidong', 59: 'mangguoxiaolao', 60: 'meiniye', 61: 'mengniu', 62: 'mengniuzaocan',
    63: 'moliqingcha', 64: 'nfc', 65: 'niudufen', 66: 'niunai', 67: 'nongfushanquan',
    68: 'qingdaowangzi-1', 69: 'qingdaowangzi-2', 70: 'qinningshui', 71: 'quchenshixiangcao',
    72: 'rancha-1', 73: 'rancha-2', 74: 'rousongbing', 75: 'rusuanjunqishui', 76: 'suanlafen',
    77: 'suanlaniurou', 78: 'taipingshuda', 79: 'tangdaren', 80: 'tangdaren2', 81: 'tangdaren3',
    82: 'ufo', 83: 'ufo2', 84: 'wanglaoji', 85: 'wanglaoji-c', 86: 'wangzainiunai', 87: 'weic',
    88: 'weitanai', 89: 'weitanai2', 90: 'weitanaiditang', 91: 'weitaningmeng', 92: 'weitaningmeng-bottle',
    93: 'weiweidounai', 94: 'wuhounaicha', 95: 'wulongcha', 96: 'xianglaniurou', 97: 'xianguolao',
    98: 'xianxiayuban', 99: 'xuebi', 100: 'xuebi-b', 101: 'xuebi2', 102: 'yezhi', 103: 'yibao',
    104: 'yida', 105: 'yingyangkuaixian', 106: 'yitengyuan', 107: 'youlemei', 108: 'yousuanru',
    109: 'youyanggudong', 110: 'yuanqishui', 111: 'zaocanmofang', 112: 'zihaiguo'
}

CLASS_NAMES_CN = {
    0: '3+2饼干', 1: '三加二', 2: '阿尔卑斯', 3: '安慕希', 4: '奥妙',
    5: '阿萨姆', 6: '白茶', 7: '百事可乐', 8: '百事可乐-2', 9: '爆矿力',
    10: '冰红茶', 11: '冰淇淋牛奶', 12: '冰糖雪梨', 13: '布丁', 14: '茶萃',
    15: '茶派', 16: '茶派2', 17: '大麦茶', 18: '道饭点1', 19: '道饭点2',
    20: '道饭点3', 21: '道饭点4', 22: '东鹏特饮', 23: '东鹏-B', 24: '芬达',
    25: '古早味', 26: '果粒橙', 27: '果粒橙2', 28: '海太', 29: '好丽友',
    30: '好丽友', 31: '和味道', 32: '和味道2', 33: '和味道3', 34: '红牛',
    35: '红牛2', 36: '红烧牛肉', 37: '尖椒', 38: '健力宝', 39: '金典', 40: '咖啡',
    41: '烤面筋-咖喱', 42: '烤面筋-椒盐', 43: '烤面筋-烧烤', 44: '烤面筋-香葱',
    45: '可比克', 46: '可乐', 47: '可乐-B', 48: '可乐-B-2', 49: '老坛酸菜',
    50: '凉面', 51: '力保健', 52: '零度可乐', 53: '零度可乐-B', 54: '李子园',
    55: '鲁花香', 56: '鹿角咖啡', 57: '卤香牛肉', 58: '脉动', 59: '芒果小酪',
    60: '美年达', 61: '蒙牛', 62: '蒙牛早餐', 63: '茉莉清茶', 64: 'NFC果汁',
    65: '牛肚粉', 66: '牛奶', 67: '农夫山泉', 68: '青岛王子-1', 69: '青岛王子-2',
    70: '沁柠水', 71: '屈臣氏香草', 72: '燃茶-1', 73: '燃茶-2', 74: '肉松饼',
    75: '乳酸菌汽水', 76: '酸辣粉', 77: '酸烂牛肉', 78: '太平梳打', 79: '汤达人',
    80: '汤达人2', 81: '汤达人3', 82: 'UFO', 83: 'UFO2', 84: '王老吉', 85: '王老吉-C',
    86: '旺仔牛奶', 87: '维C', 88: '维他奶', 89: '维他奶2', 90: '维他奶低糖',
    91: '维他柠檬', 92: '维他柠檬-瓶装', 93: '维维豆奶', 94: '午后奶茶', 95: '乌龙茶',
    96: '香兰牛肉', 97: '鲜果酪', 98: '鲜虾鱼板', 99: '雪碧', 100: '雪碧-B',
    101: '雪碧2', 102: '椰汁', 103: '怡宝', 104: '益达', 105: '营养快线',
    106: '一藤园', 107: '优乐美', 108: '优酸乳', 109: '优洋果冻', 110: '元气水',
    111: '早餐魔方', 112: '自嗨锅'
}


def get_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS goods (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            label TEXT,
            price REAL NOT NULL DEFAULT 0,
            stock INTEGER NOT NULL DEFAULT 0,
            is_deleted INTEGER NOT NULL DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id TEXT PRIMARY KEY,
            goods_info TEXT,
            total_price REAL NOT NULL DEFAULT 0,
            order_time TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending'
        )
    ''')

    cursor.execute('SELECT COUNT(*) FROM goods')
    if cursor.fetchone()[0] == 0:
        for idx in range(113):
            cursor.execute(
                'INSERT INTO goods (id, name, label, price, stock, is_deleted) VALUES (?, ?, ?, ?, ?, ?)',
                (str(uuid.uuid4()), CLASS_NAMES_CN[idx], idx, 0, 0, 0)
            )

    conn.commit()
    conn.close()


class GoodsManager:
    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM goods WHERE is_deleted = 0')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def add(name, label, price=0):
        conn = get_connection()
        cursor = conn.cursor()
        gid = str(uuid.uuid4())
        cursor.execute('INSERT INTO goods (id, name, label, price, stock, is_deleted) VALUES (?, ?, ?, ?, 0, 0)',
                       (gid, name, label, price))
        conn.commit()
        conn.close()
        return gid

    @staticmethod
    def update(gid, name, label, price):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE goods SET name=?, label=?, price=? WHERE id=?', (name, label, price, gid))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(gid):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE goods SET is_deleted=1 WHERE id=?', (gid,))
        conn.commit()
        conn.close()

    @staticmethod
    def update_stock(label, count):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE goods SET stock=? WHERE label=?', (count, label))
        conn.commit()
        conn.close()

    @staticmethod
    def get_by_label(label):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM goods WHERE label=? AND is_deleted=0', (label,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None


class OrdersManager:
    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM orders ORDER BY order_time DESC')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def create(goods_info_list, total_price, status='Pending'):
        conn = get_connection()
        cursor = conn.cursor()
        oid = str(uuid.uuid4())
        order_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        goods_json = json.dumps(goods_info_list, ensure_ascii=False)
        cursor.execute(
            'INSERT INTO orders (id, goods_info, total_price, order_time, status) VALUES (?, ?, ?, ?, ?)',
            (oid, goods_json, total_price, order_time, status)
        )
        conn.commit()
        conn.close()
        return oid

    @staticmethod
    def get_detail(oid):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM orders WHERE id=?', (oid,))
        row = cursor.fetchone()
        conn.close()
        if row:
            result = dict(row)
            result['goods_info'] = json.loads(result['goods_info']) if result['goods_info'] else []
            return result
        return None


REVERSE_CLASS_MAPPING = {v: k for k, v in CLASS_MAPPING.items()}


def analyze_images(before_img_path, after_img_path, model, conf=0.5, iou=0.6):
    before_results = model(before_img_path, conf=conf, iou=iou)
    after_results = model(after_img_path, conf=conf, iou=iou)

    print(f"model.names = {model.names}")

    before_counts = {}
    if before_results[0].boxes is not None:
        for box in before_results[0].boxes:
            cls = int(box.cls[0].item())
            before_counts[cls] = before_counts.get(cls, 0) + 1

    after_counts = {}
    if after_results[0].boxes is not None:
        for box in after_results[0].boxes:
            cls = int(box.cls[0].item())
            after_counts[cls] = after_counts.get(cls, 0) + 1

    print(f"before_counts = {before_counts}")
    print(f"after_counts = {after_counts}")

    purchased = []
    for cls_id, before_count in before_counts.items():
        after_count = after_counts.get(cls_id, 0)
        diff = before_count - after_count
        if diff > 0:
            goods = GoodsManager.get_by_label(cls_id)
            if goods:
                purchased.append({
                    'label': goods['label'],
                    'name': goods['name'],
                    'quantity': diff,
                    'price': goods['price'],
                    'subtotal': diff * goods['price']
                })

    total = sum(item['subtotal'] for item in purchased)
    status = 'Completed' if purchased else 'Cancelled'

    before_display = {}
    for cls_id, count in before_counts.items():
        goods = GoodsManager.get_by_label(cls_id)
        if goods:
            before_display[goods['name']] = count

    after_display = {}
    for cls_id, count in after_counts.items():
        goods = GoodsManager.get_by_label(cls_id)
        if goods:
            after_display[goods['name']] = count

    return purchased, total, status, before_display, after_display
