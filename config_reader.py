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
        self.config_file = Path(__file__).parent.parent /'config'/ 'settings.yaml'
        with open(self.config_file,'r') as f:
            self.data = yaml.safe_load(f)

    def get(self,key):
        return self.data.get(key)

config = Config()


