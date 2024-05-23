import configparser
import os
import settings

class Config:
    def __init__(self, filepath=''):
        self.config = configparser.ConfigParser()
        self.filepath = filepath if filepath else os.path.join(os.path.dirname(__file__), '..', 'config.ini')
        self._validate_filepath()
        self._read_and_parse_config()
        self.load_config()

    def parse_cookie_string(self, cookie_string):
        cookies = {}
        parts = cookie_string.split(';')
        for part in parts:
            try:
                key, value = part.strip().split('=', 1)
                cookies[key] = value
            except ValueError:
                print(f"Skipping malformed cookie part: {part}")
                continue
        return cookies

    def _validate_filepath(self):
        if not os.path.isfile(self.filepath):
            raise FileNotFoundError(f"Config file not found at: {self.filepath}")

    def _read_and_parse_config(self):
        with open(self.filepath, 'r') as file:
            config_content = file.read()
        safe_config_content = config_content.replace('%', '%%')
        self.config.read_string(safe_config_content)

    def load_config(self):
        # 读取 cookie 字符串
        cookie_string = self.config.get('boss', 'cookie', fallback='')
        self.cookie = self.parse_cookie_string(cookie_string)
        # 加载其他配置
        self.jobs_id = self.config.get('boss', 'jobs_id', fallback='').split(',')
        self.job_name = self.config.get('boss', 'job_name', fallback='')
        self.experience = self.config.get('boss', 'experience', fallback='')
        self.educational_level = self.config.get('boss', 'educational_level', fallback='')
        self.geek_list_url = self.config.get('boss', 'geek_list_url', fallback='')
        self.geek_info_url = self.config.get('boss', 'geek_info_url', fallback='')
        self.job_detail_url = self.config.get('boss', 'job_detail_url', fallback='')
        self.chat_start_url = self.config.get('boss', 'chat_start_url', fallback='')
        # 大模型相关配置
        settings.MODEL = self.config.get('default', 'model', fallback='')
        settings.MODEL_BASE_URL = self.config.get('default', 'model_base_url', fallback='')
    