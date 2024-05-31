'''
app/__init__.py文件
    4.1 设置项目名称
    4.2 设置数据库连接
    4.3 设置项目缓存
    4.4 设置DEBUG模式
    4.5 数据库连接
    4.6 设置缓存机制
    4.7 设置蓝图(提高编程效率)
'''
import os
# 1.导入flask框架 render_template读取视图文件
from flask import Flask,render_template
# 2.导入数据库连接模块
from flask_sqlalchemy import  SQLAlchemy
# 3.导入flask框架缓存模块
from flask_redis import  FlaskRedis

# 设置作者
__author__ = "zpp"
'''
1.设置项目名称
    将Flask框架的类实例化对象
'''
app = Flask(__name__)
'''
2.数据库连接设置
mysql+mysqlconnector ===>mysql数据库+mysql数据库驱动模块
root:mysql ===>用户名和密码
127.0.0.1:3306 ===>ip地址和端口号
movie ===>数据库名称
'''
# 2.1 设置mysql连接参数
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql+mysqlconnector://root:mysql@127.0.0.1:3306/movie'

# 2.2 设置mysql对象修改与信号发送
# 将数据映射到Flask框架中进行缓存
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
'''
3.设置项目缓存
'''
# 3.1 设置缓存的url
app.config['REDIS_URL'] = 'redis://127.0.0.1:6379/0'

# 3.2 设置秘钥
app.config['SECRET_KEY'] = 'zpp_movie'

# 3.3 设置后端上传的目录
# os.path.abspath ===>D:\PycharmProjects\JSNUMovie2024\app
# os.path.dirname(__file__) ===> zpp.wav
# static/uploads
# D:\PycharmProjects\JSNUMovie2024\app\static\uploads\zpp.wav
app.config['UP_DIR'] = \
    os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'static/uploads/'
    )

# 3.4 设置前端上传路径
app.config['FC_DIR'] = \
    os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'static/uploads/user/'
    )

'''
4.设置DEBUG模式
'''
app.debug = False

'''
5.数据库连接变量
将数据库的驱动和Flask对象关联
'''
db = SQLAlchemy(app)

'''
6.设置缓存机制变量
'''
rd = FlaskRedis(app)

'''
7.设置蓝图
相当于 web.xml 127.0.0.1/zpp/admin/toLogin.do
'''
# 7.1 导入蓝图 admin是后台管理请求部分
from app.admin import admin as  admin_blueprint

# 7.2 注册蓝图
# 127.0.0.1:5000/admin ====>跳转到后台管理系统部分
# 127.0.0.1:5000/home  ====>跳转到前台显示系统部分
app.register_blueprint(admin_blueprint,
                       url_prefix='/admin')
