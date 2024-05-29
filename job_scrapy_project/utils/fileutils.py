import os, pickle
from utils.logger import log

def get_file_content(filename):
    _ = []
    with open(filename, 'a+') as f:
        f.seek(0)
        ls = f.readlines()
        for l in ls:
            _.append(l.strip())
    return _

def save_data_to_file(filename, data, m='a+'):
    # 确保文件所在的目录存在
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, m) as f:
        f.write(data.strip() + '\n')

def load_obj_from_file(filename, m='rb'):
    """
    从文件读对象
    """
    _ = None
    try:
        with open(filename, m) as f:
            _ = pickle.load(f)
    except:
        log(f'读取文件[{filename}]失败')
        return None
    return _

def save_obj_to_file(obj, filename, m='wb'):
    """
    把对接存入文件
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, m) as f:
        pickle.dump(obj, f)
