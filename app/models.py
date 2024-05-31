'''
app/models.py文件
该文件admin和 home两个蓝图共有的文件
模型
'''
# 在app/__init__.py中  db对象
from app import db
from datetime import datetime
# 1.管理员
class Admin(db.Model):
    # 1.1 设置表名称(数据库表名一致)
    __tablename__ = 'admin'
    # 1.2 判断表是否存在
    table_args = {'useexisting':True}
    # 1.3 设置映射
    id = db.Column(db.Integer,primary_key=True) # 编号
    name = db.Column(db.String(100),unique=True) # 管理员账号
    pwd = db.Column(db.String(100)) # 管理员密码
    is_super = db.Column(db.SmallInteger) # 是否为管理员0,1
    role_id = db.Column(db.Integer,db.ForeignKey("role.id")) #角色id
    addtime = db.Column(db.DateTime,index=True,
                      default=datetime.now())
    # 1.4 外键关联
    adminlogs = db.relationship("Adminlog",backref='admin') # 管理员登录日志
    oplogs = db.relationship("Oplog",backref='admin') # 管理员操作日志

    # 1.5 设置对象属性
    def __repr__(self):
        return "<Admin %r>"%self.name
    # 1.6 检查密码
    def check_pwd(self,userPwd):
        return self.pwd == userPwd

# 2.管理员登录日志
class Adminlog(db.Model):
    # 2.1 设置映射表的名称
    __tablename__ = 'adminlog'
    # 2.2 设置表必须存在
    table_args = {'useexisting':True}
    # 2.3 设置映射关系
    id = db.Column(db.Integer,primary_key=True)
    admin_id = db.Column(db.Integer,db.ForeignKey('admin.id'))
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime,index=True,
                        default=datetime.now())
    # 2.4 设置返回值
    def __repr__(self):
        return "<Adminlog %r>"%self.id

# 3.标签表
class Tag(db.Model):
    __tablename__ = 'tag'
    table_args = {'useexisting':True}
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),unique=True)
    addtime = db.Column(db.DateTime,index=True,
                        default=datetime.now())
    # 设置外键关联
    movies = db.relationship("Movie",backref='tag')
    def __repr__(self):
        return "<Tag  %r>"%self.name

# 4.管理员操作日志
class Oplog(db.Model):
    # 4.1 设置表名
    __tablename__ = 'oplog'
    # 4.2 设置必须存在
    table_args = {'useexisting':True}
    # 4.3 设置映射关系
    id = db.Column(db.Integer,primary_key=True)
    admin_id = db.Column(db.Integer,db.ForeignKey('admin.id'))
    ip = db.Column(db.String(100)) # ip地址
    reason = db.Column(db.String(100)) #操作原因
    addtime = db.Column(db.DateTime,index=True,
                            default=datetime.now())
    # 4.4 返回值
    def __repr__(self):
        return "<Oplog %r>"%self.id
# 5.角色表
class Role(db.Model):
    # 5.1  设置表名
    __tablename__ = "role"
    # 5.2 设置必须存在
    table_args = {'useexisting',True}
    # 5.3 设置映射关系
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),unique=True)
    auths = db.Column(db.String(100)) # 角色权限列表
    addtime = db.Column(db.DateTime,index=True,
                        default=datetime.now())
    # 5.4  设置外键关联
    admins = db.relationship('Admin',backref='role')# 管理员外键关联

    # 5.5 返回值
    def __repr__(self):
        return "<Role %r>"%self.name

# 6.电影表
class Movie(db.Model):
    # 6.1 设置表名
    __tablename__ = 'movie'
    # 6.2 设置表必须存在
    table_args = {'useexisting':True}
    # 6.3 设置映射关系(id必须跟表字段名一致)
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(255),unique=True)
    url = db.Column(db.String(255),unique=True)
    info = db.Column(db.Text)
    logo = db.Column(db.String(255),unique=True)
    star = db.Column(db.SmallInteger)
    playnum = db.Column(db.BigInteger)
    commentnum = db.Column(db.BigInteger)

    tag_id = db.Column(db.Integer,db.ForeignKey('tag.id'))
    area = db.Column(db.String(255)) # 地区
    release_time = db.Column(db.Date) # 上映时间
    length = db.Column(db.String(100)) # 影片播放时长
    addtime  = db.Column(db.DateTime,index=True,
                         default=datetime.now())
    # 6.4 评论和收藏表外键关联
    comments = db.relationship("Comment",backref='movie') # 评论
    moviecols = db.relationship("Moviecol",backref='movie')# 收藏

    # 6.5 返回值
    def  __repr__(self):
        return "<Movie %r>"%self.title

# 7.预告表
class Preview(db.Model):
    __tablename__ = 'preview'
    table_args = {'useexisting':True}
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(255),unique=True)
    logo = db.Column(db.String(255),unique=True)
    addtime = db.Column(db.DateTime,index=True,
                        default=datetime.now())
    def __repr__(self):
        return "<Preview %r>"%self.title

# 8.会员表
class User(db.Model):
    __tablename__ = 'user'
    table_args = {'useexisting':True}
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255),unique=True)
    pwd = db.Column(db.String(255))
    email = db.Column(db.String(255),unique=True)
    phone = db.Column(db.String(11),unique=True)
    info = db.Column(db.Text)
    face  = db.Column(db.String(255),unique=True)
    addtime = db.Column(db.DateTime,index=True,
                        default=datetime.now())
    uuid  = db.Column(db.String(255),unique=True)

    # 评论电影收藏
    comments = db.relationship("Comment",backref='user')
    moviecols = db.relationship("Moviecol", backref='user')
    userlogs = db.relationship("Userlog", backref='user')

# 9.评论表
class Comment(db.Model):
    __tablename__ = 'comment'
    table_args = {'useexisting':True}
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.Text)
    movie_id = db.Column(db.Integer,db.ForeignKey("movie.id"))
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    addtime = db.Column(db.DateTime,index=True,
                        default=datetime.now())
    def __repr__(self):
        return "<Comment %r>"%self.id

# 10.收藏表
class Moviecol(db.Model):
    __tablename__ = 'moviecol'
    table_args = {'useexisting':True}
    id = db.Column(db.Integer,primary_key=True)
    movie_id = db.Column(db.Integer,db.ForeignKey('movie.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    addtime = db.Column(db.Integer,index=True,
                        default=datetime.now())
    def __repr__(self):
        return "<Moviecol %r>"%self.id

# 11.会员登录日志
class Userlog(db.Model):
    __tablename__ = 'userlog'
    table_args = {'useexisting':True}
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime,index=True,
                       default=datetime.now())
    def __repr__(self):
        return "<Userlog %r>"%self.id

# 12.权限
class Auth(db.Model):
    __tablename__ = 'auth'
    table_args = {'useexisting':True}
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255),unique=True)
    url = db.Column(db.String(255),unique=True)
    addtime = db.Column(db.DateTime,index=True,
                        default=datetime.now())

    def __repr__(self):
        return "<Auth %r>"%self.name

