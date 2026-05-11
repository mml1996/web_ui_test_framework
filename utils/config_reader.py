# -------------做什么

###  编写配置文件与读取器

###  读取配置文件  ###

#-------------为什么这么做

###  封装成config类便于全局访问

###  作用
###  实现配置与代码分离，提升框架灵活性和维护性


import yaml
from pathlib import Path


class Config:
    def __init__(self):
        self.config_file = Path(__file__).parent.parent / 'config' / 'settings.yaml'

        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.data = yaml.safe_load(f)
            if not self.data:
                raise ValueError("配置文件为空")
        except FileNotFoundError:
            raise FileNotFoundError(f"配置文件不存在: {self.config_file}")
        except Exception as e:
            raise Exception(f"读取配置文件失败: {str(e)}")

    def get(self, key, default=None):
        """
        获取配置值
        :param key: 配置项名称
        :param default: 配置项不存在时返回的默认值
        :return: 配置值
        """
        return self.data.get(key, default)


# 全局配置实例
config = Config()


