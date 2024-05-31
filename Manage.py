'''
项目运行的主入口
Manage.py
'''
from flask_script import Manager
from app import app
# 1.设置业务管理文件(app是一个Flask类的实例化对象)
MG = Manager(app)

if __name__ == '__main__':
    MG.run()
