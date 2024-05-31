'''
app/admin/__init__.py
'''
from flask  import  Blueprint
# 设置当前模块的蓝图 名称为admin
admin = Blueprint('admin',__name__)

# 设置当前蓝图的视图管理文件
import app.admin.views