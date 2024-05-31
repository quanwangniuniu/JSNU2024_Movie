'''
app/admin/forms.py
借助第三方插件实现表单验证 wtforms
wtforms是一个支持多种web框架的form组件,主要用于对用户请求数据处理验证
Forms:主要表单验证、字段定义、HTML生成,并将各种验证流程聚在一起
'''
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,FileField,TextAreaField,SelectField
from wtforms.validators import DataRequired
from app.models import Tag
# 1.管理员登录表单
class LoginForm(FlaskForm):
    # 1.1 账户
    # account名称必须和login.html中 form.account一致
    account = StringField(
        label="账户",
        validators=[DataRequired("账户不能为空")],
        description="管理员账户",
        render_kw={
            'class':'form-control',
            'placeholder':"请输入管理员账户"
        }
    )
    # 1.2 密码
    pwd = PasswordField(
        label="密码",
        validators=[DataRequired("密码不能为空")],
        description="管理员密码",
        render_kw={
            'class': 'form-control',
            'placeholder': "请输入管理员密码"
        }
    )
    # 1.3 登录按钮
    submit = SubmitField(
        label="登录",
        render_kw = {
            'class':'btn btn-primary btn-block btn-flat'
        }
    )

# 2.标签表单
class TagForm(FlaskForm):
    name = StringField(
        label="电影标签",
        validators=[DataRequired('标签名不能为空')],
        description="电影标签",
        render_kw={
            'class':'form-control',
            'id':'input_name',
            'placeholder':'请输入电影标签名称!!!'
        }
    )
    submit = SubmitField(
        label="添加标签",
        render_kw={
            'class':'btn btn-primary'
        }
    )

# 3.电影表单
class MovieForm(FlaskForm):
    # 3.1 标题
    title  = StringField(
        label="片名",
        validators=[DataRequired("片名不能为空")],
        description="电影名称",
        render_kw={
            'class':'form-control',
            'id':'input_title',
            'placeholder':'请输入电影名称'
        }
    )
    # 3.2 电影存储路径(本地路径)
    url = FileField(
        label="电影文件",
        validators=[DataRequired("请上传文件")],
        description="电影文件"
    )
    # 3.3  电影的简介
    info = TextAreaField(
        label='电影简介',
        validators=[DataRequired('简介不能为空')],
        description='电影简介',
        render_kw={
            'class':'form-control',
            'rows':10
        }
    )
    # 3.4 电影海报
    logo = FileField(
        label='电影封面',
        validators=[DataRequired('请上传海报')],
        description='电影封面'
    )
    # 3.5 电影星级
    star = SelectField(
        label="星级",
        validators=[DataRequired('请选择星级')],
        coerce=int,
        choices=[(1,'1星'),(2,'2星'),(3,'3星'),
                 (4,'4星'),(5,'5星')],
        description="星级",
        render_kw={
            'class':'form-control'
        }
    )
    # 3.6 电影的标签
    tag_id = SelectField(
        label="电影标签",
        validators=[DataRequired('请选择电影标签')],
        coerce=int,
        # 查询数据库中tag标签表的内容循环遍历
        # (1,‘冒险’) (2,'喜剧')
        choices=[(v.id,v.name) for v in Tag.query.all()],
        description="电影标签",
        render_kw={
            'class':'form-control'
        }
    )
    # 3.7 地区
    area = StringField(
        label="地区",
        validators=[DataRequired("请输入地区")],
        description="地区",
        render_kw={
            'class':'form-control',
            'placeholder':'请输入地区'
        }
    )
    # 3.8 电影时长
    length = StringField(
        label="电影时长",
        validators=[DataRequired('片长不能为空!')],
        description='电影时长',
        render_kw={
            'class':'form-control',
            'placeholder':'请输入电影时长!!!!'
        }
    )
    # 3.9  上映时间
    release_time = StringField(
        label='上映时间',
        validators=[DataRequired("上映时间不能为空！！！")],
        description="上映时间",
        render_kw={
            'class': 'form-control',
            'placeholder': '请选择上映时间',
            'id':'input_release_time'
        }
    )
    # 3.10 按钮
    submit = SubmitField(
        label="添加电影",
        render_kw={
            'class': 'btn btn-primary',
        }
    )

# 4.预告表单
class PreviewForm(FlaskForm):
    title = StringField(
        label="预告标题",
        validators=[DataRequired("预告标题不能为空")],
        description="上映电影的预告标题",
        render_kw={
            'class':'form-control',
            'placeholder':'请输入预告标题'
        }
    )
    logo = FileField(
        label="预告封面",
        validators=[DataRequired('预告封面不能为空')],
        description='预告封面'
    )
    submit = SubmitField(
        label="添加预告",
        render_kw={
            'class':'btn btn-primary'
        }
    )

# 5.权限表单
class AuthForm(FlaskForm):
    name = StringField(
        label="权限名称",
        validators=[DataRequired('权限名称不能为空')],
        description="权限名称",
        render_kw={
            'class':'form-control',
            'placeholder':'请输入权限名称'
        }
    )
    url =  StringField(
        label="权限地址",
        validators=[DataRequired('权限地址不能为空')],
        description="权限地址",
        render_kw={
            'class':'form-control',
            'placeholder':'请输入权限地址'
        }
    )
    submit = SubmitField(
        label="添加",
        render_kw={
            'class':'btn btn-primary'
        }
    )