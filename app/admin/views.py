'''
app/admin/views.py
'''
import os
import stat
import uuid

from . import admin # 导入当前的蓝图admin
from flask import render_template,flash,url_for,redirect,session,request # 导入连接视图功能
from app.admin.forms import LoginForm,TagForm,MovieForm,PreviewForm,AuthForm
from app.models import Admin,Adminlog,Tag,Movie,Preview,User,Comment,Moviecol,Oplog,Auth,Userlog
from app import  db
from app import app
from werkzeug.utils import secure_filename
from datetime import datetime

# 1.登录模块功能实现
# 127.0.0.1:5000/admin/login  GET,POST都使用下面函数接收
# @admin是蓝图名称 对应的app/admin/__init__.py中的设置
@admin.route("/login/",methods=['GET','POST'])
def login():
    # 1.获取登录页面表单
    form = LoginForm()
    # 2.判断表单是否提交
    if form.validate_on_submit():
        # 3.获取表单数据
        data = form.data
        # 4.根据account查询用户对象是否存在
        # 根据account值查询admin数据==>将数据保存到admin的模型中
        admin = Admin.query.filter_by(name=data['account'])\
            .first()
        # 5.判断查询的数据是否为空
        if admin == None or \
            not admin.check_pwd(data['pwd']):
            # 5.1 通过flash发送错误信息
            flash("用户名或密码错误",'err')
            # 5.2 重定向请求 /admin/login
            return redirect(url_for("admin.login"))
        # 6.用户名和密码一致的则保存数据到session中
        session['admin'] = data['account']
        session['admin_id'] = admin.id
        # 7.设置管理员登录日志
        adminlog = Adminlog(
            admin_id=admin.id,
            ip = request.remote_addr
        )
        # 8.数据库添加操作
        db.session.add(adminlog)
        db.session.commit()
        # 9.重定向到主页面
        return redirect(url_for("admin.index"))

    return render_template("admin/login.html",form=form)

# 2.后台管理系统首页
@admin.route("/")
def index():
    return render_template("admin/index.html")

# 3.标签管理-添加标签
@admin.route("/tag_add/",methods=['GET','POST'])
def tag_add():
    '''
    GET 请求 返回html页面
    POST 请求 接收form表单数据
    '''
    # 3.1 获取Tag表单
    form = TagForm()
    # 3.2 判断是否点击表单提交
    if form.validate_on_submit():
        # 3.3 获取表单数据
        data = form.data
        # 3.4 根据标签名查找统计标签
        tag = Tag.query.filter_by(name=data['name']).count()
        # 3.5 判断是否查找到该标签
        if tag == 1:
            flash("电影标签已存在,不可重复",'err')
            return redirect(url_for("admin.tag_add"))
        # 3.6 设置tag模型(实体类)
        tag = Tag(name=data['name'])
        # 3.7 设置session添加
        db.session.add(tag)
        db.session.commit()
        # 3.8 设置oplog模型
        # oplog = Oplog(
        #     admin_id = session['admin_id'],
        #     ip = request.remote_addr,
        #     reason='添加标签%s'%data['name']
        # )
        # 3.9 添加管理员操作日志
        # db.session.add(oplog)
        # db.session.commit()
        # 3.10 弹出成功提示框
        flash("标签添加成功",'ok')
        redirect(url_for("admin.tag_add"))

    return render_template("admin/tag_add.html",
                           form=form)

# 4.标签管理-标签列表
@admin.route("/tag_list/<int:page>",methods=['GET'])
def tag_list(page=None):
    # 4.1 无页码情况
    if page is None:
        page = 1
    # 4.2 有页码情况 per_page 每页显示的条目数
    page_data = Tag.query.order_by(Tag.addtime) \
            .paginate(page=page,per_page=5)
    # 4.3 返回页面
    return render_template("admin/tag_list.html",
                           page_data=page_data)

# 5.标签管理-编辑标签
@admin.route("/tag_edit/<int:id>",methods=['GET','POST'])
def tag_edit(id=None):
    # 5.1 获取表单
    form = TagForm()
    # 5.2 根据id获取标签对象
    tag = Tag.query.get_or_404(id)
    # 5.3 修改表单中的按钮名称
    form.submit.label.text = "修改标签"
    # 5.4 判断修改按钮是否点击提交
    if form.validate_on_submit():
        # 5.5 获取表单数据
        data = form.data
        # 5.6 查询修改标签数据是否已存在
        tag_count = Tag.query.filter_by(name=data['name'])\
                    .count()
        # 5.7 判断(名称不一致 修改  且修改后名称查询得到数量1)
        if tag.name != data['name']\
            and tag_count == 1:
            flash("标签名称已存在!!",'err')
            return redirect(url_for('admin.tag_edit',id=tag.id))
        # 5.8 将表单中的数据进行修改
        tag.name = data['name']
        # 5.9 数据库数据修改 (tag对象中已经存在tag.id如果一致则代表修改)
        db.session.add(tag)
        db.session.commit()
        # 5.10 提示框
        flash("标签已经修改成功",'ok')
        # 5.11 重定向到编辑页面
        redirect(url_for('admin.tag_edit',id=tag.id))

    return render_template("admin/tag_edit.html",
                           form = form,tag = tag)

# 6.标签管理-删除标签
@admin.route("/tag_del/<int:id>",methods=['GET'])
def tag_del(id=None):
    #  6.1 根据id查询标签数据
    tag = Tag.query.filter_by(id=id).first_or_404()
    # 6.2 如果数据库中有该标签则删除
    db.session.delete(tag)
    db.session.commit()
    # 6.3  提示框
    flash("标签<<<{0}>>>删除成功".format(tag.name),'ok')
    # 6.4 重定向标签列表页面
    return redirect(url_for('admin.tag_list',page=1))

# 7.电影管理-电影添加
@admin.route("/movie_add/",methods=['GET','POST'])
def movie_add():
    # 7.1 获取电影表单
    form = MovieForm()
    # 7.2 判断是否点击提交
    if form.validate_on_submit():
        # 7.3 获取表单数据
        data = form.data
        # 7.4 处理电影文件以及LOGO上传
        file_url = secure_filename(form.url.data.filename)
        file_logo = secure_filename(form.logo.data.filename)
        # 7.5 判断uploads是否存在 static/uploads
        if not os.path.exists(app.config['UP_DIR']):
            # 7.5.1 创建目录
            os.mkdir(app.config['UP_DIR'])
            # 7.5.2 修改目录权限
            os.chmod(app.config['UP_DIR'],stat.S_IRWXU)
        # 7.6 更改路径以及名称等
        url = change_filename(file_url)
        logo = change_filename(file_logo)
        # 7.7 保存数据到form表单中
        # form.url = 'static/uploads/20240520163730131231221312.wav'
        form.url.data.save(app.config['UP_DIR']+url)
        form.logo.data.save(app.config['UP_DIR']+logo)
        # 7.8 设置模型对象数据
        movie  = Movie(
            title=data['title'],
            url = url,
            info = data['info'],
            logo = logo,
            star = int(data['star']),
            playnum = 0,
            commentnum = 0,
            tag_id = int(data['tag_id']),
            area = data['area'],
            release_time = data['release_time'],
            length = data['length']
        )
        # 7.9 添加数据
        db.session.add(movie)
        db.session.commit()
        # 7.10 弹出框
        flash("添加电影成功啦啦啦!!!",'ok')
        # 7.11 重定向
        return redirect(url_for("admin.movie_add"))

    return render_template('admin/movie_add.html',
                           form=form)

# 8.电影管理-电影列表
@admin.route("/movie_list/<int:page>",methods=['GET'])
def movie_list(page=None):
    # 8.1 判断page是否有值
    if page is None:
        page = 1
    # 8.2 进行关联查询
    # join() 关联查询 Tag标签表
    # filter 多表关联字段查询
    page_data = Movie.query.join(Tag).filter(
        Tag.id == Movie.tag_id
    ).order_by(
        Movie.addtime.desc()
    ).paginate(page=page,per_page=5)
    # 8.3 返回movie_list.html
    return render_template("admin/movie_list.html",
                           page_data=page_data)

# 9.电影管理-电影编辑
@admin.route("/movie_edit/<int:id>",methods=['GET','POST'])
def movie_edit(id=None):
    # 9.1 获取电影表单
    form = MovieForm()
    # 9.2 读取url,logo非空验证为空,编辑不修改的时候
    form.url.validators = []
    form.logo.validators = []
    form.submit.label.text = "编辑电影"
    # 9.3 根据id查询数据
    movie = Movie.query.get_or_404(int(id))

    # 9.4 判断请求的类型
    if request.method == 'GET':
        # 9.5 设置info,tag_id,star数据
        form.info.data = movie.info
        form.tag_id.data = movie.tag_id
        form.star.data = movie.star
    # 9.6 表单是否点击提交
    if form.validate_on_submit():
        print("进入表单提交")
        # 9.7 获取表单数据
        data = form.data
        # 9.8 根据表单名称查询数据库是否存在
        movie_count = \
            Movie.query.filter_by(title=data['title']).count()
        # 9.9 判断电影名称是否存在以及电影名称是否修改
        if movie_count == 1 and \
            movie.title != data['title']:
            flash("片名已经存在!",'err')
            return redirect(
                url_for("admin.movie_edit",id=id))
        # 9.10 创建目录
        if not os.path.exists(app.config['UP_DIR']):
            os.mkdir(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'],stat.S_IRWXU)


        # 9.11 上传新的视频文件
        # if form.url.data !=  "":
        if form.url.data.filename != '':
            # 删除原有的视频文件
            os.remove(app.config['UP_DIR']+movie.url)
            # 上传新的视频文件
            file_url  = secure_filename(form.url.data.filename)
            # 修改新的视频文件名称
            movie.url = change_filename(file_url)
            # 将新的视频文件名称保存到form表单中
            form.url.data.save(app.config['UP_DIR']+movie.url)

        # 9.12 上传图片
        # if form.logo.data != "":
        if form.logo.data.filename != "":
            # 删除原有的图片文件
            os.remove(app.config['UP_DIR']+movie.logo)
            # 上传图片的文件名称
            file_logo = secure_filename(form.logo.data.filename)
            # 修改上传图片的文件名称
            movie.logo = change_filename(file_logo)
            # 保存新的图片名称到表单中
            form.logo.data.save(app.config['UP_DIR']+movie.logo)

        # 9.13 设置其他的 数据信息
        movie.star = data['star']
        movie.tag_id = data['tag_id']
        movie.info = data['info']
        movie.title = data['title']
        movie.area = data['area']
        movie.length = data['length']
        movie.release_time = data['release_time']
        # 9.14 数据提交修改
        db.session.add(movie)
        db.session.commit()
        # 9.15 提示框
        flash("修改电影成功啦啦啦!!!",'ok')
        return redirect(url_for('admin.movie_edit',id=id))


    return render_template("admin/movie_edit.html",
                           form = form,movie=movie)

# 10.电影管理-电影删除
@admin.route("/movie_del/<int:id>",methods=['GET','POST'])
def movie_del(id=None):
    # 10.1 查看是否存在该电影
    movie = Movie.query.get_or_404(id)
    # 10.2 删除电影
    if not movie is None:
        # 10.3 删除电影文件以及电影海报
        os.remove(app.config['UP_DIR']+movie.url)
        os.remove(app.config['UP_DIR']+movie.logo)
        # 10.4 删除电影对象
        db.session.delete(movie)
        db.session.commit()
        # 10.5 提示框
        flash(f'电影<<<{movie.title}>>>删除了','ok')
        # 10.6 重定向
        return redirect(url_for("admin.movie_list",page=1))

# 11.预告管理-预告添加
@admin.route("/preview_add/",methods=['GET','POST'])
def preview_add():
    # 11.1 获取预告表单
    form = PreviewForm()
    # 11.2判断是否点击表单提交
    if form.validate_on_submit():
        # 11.3 获取表单数据
        data = form.data
        # 11.4 处理LOGO
        file_logo = secure_filename(form.logo.data.filename)
        # 11.5 判断uploads是否存在
        if not os.path.exists(app.config['UP_DIR']):
            # 11.5.1  创建目录
            os.mkdir(app.config['UP_DIR'])
            # 11.5.2 设置目录权限
            os.chmod(app.config['UP_DIR'],stat.S_IRWXU)
        # 11.6 修改logo的名称
        new_logo = change_filename(file_logo)
        # 11.7 保存数据到form中(存储到本地uploads目录中+新名称)
        form.logo.data.save(app.config['UP_DIR']+new_logo)
        # 11.8 设置模型
        preview = Preview(
            title = data['title'],
            logo = new_logo,
            addtime = datetime.now()
        )
        # 11.9 将模型添加到数据库中
        db.session.add(preview)
        db.session.commit()
        # 11.10 弹出框
        flash("添加预告成功啦!!",'ok')
        # 11.11 重定向
        return redirect(url_for('admin.preview_add'))

    return render_template("admin/preview_add.html",
                           form=form)

# 12.预告管理-预告列表
@admin.route("/preview_list/<int:page>",methods=['GET'])
def preview_list(page=None):
    # 12.1 无页码情况
    if page is None:
        page = 1
    # 12.2 有页码情况 per_page 每页显示的条目数
    page_data = Preview.query.order_by(Preview.addtime) \
            .paginate(page=page,per_page=5)
    # 12.3 返回页面
    return render_template("admin/preview_list.html",
                           page_data=page_data)

# 13.预告管理-预告编辑
@admin.route("/preview_edit/<int:id>",methods=['GET','POST'])
def preview_edit(id=None):
    # 13.1 获取表单
    form = PreviewForm()
    # 13.2  设置logo验证器为空
    form.logo.validators = []
    # 13.3 根据id获取标签对象
    preview = Preview.query.get_or_404(id)
    # 13.4 修改表单中的按钮名称
    form.submit.label.text = "修改预告"
    # 13.5 判断请求类型
    if request.method == 'GET':
        form.title.data = preview.title
    # 13.6 判断表单请求
    if form.validate_on_submit():
        # 13.7 获取表单数据
        data = form.data
        # 13.8 根据表单查询数据是否存在
        preview_count = Preview.query.filter_by(
                    title=data['title']).count()
        # 13.9 判断预告名称是否存在
        if preview_count == 1 and \
            preview.title != data['title']:
            flash("预告名称已存在",'err')
            return redirect(url_for("admin.preview_edit",id=id))
        # 13.10 判断uploads是否存在
        if not os.path.exists(app.config['UP_DIR']):
            # 13.10.1  创建目录
            os.mkdir(app.config['UP_DIR'])
            # 13.10.2 设置目录权限
            os.chmod(app.config['UP_DIR'], stat.S_IRWXU)
        # 13.11 判断海报是否上传
        if form.logo.data.filename != "":
            # 删除原有的视频文件
            os.remove(app.config['UP_DIR'] + preview.logo)
            # 上传新的视频文件
            file_url = secure_filename(form.logo.data.filename)
            # 修改新的视频文件名称
            preview.logo = change_filename(file_url)
            # 将新的视频文件名称保存到form表单中
            form.logo.data.save(app.config['UP_DIR'] + preview.logo)
        # 13.12 设置其他数据
        preview.title = data['title']
        # 13.13 数据提交修改
        db.session.add(preview)
        db.session.commit()
        flash("预告修改成功!!!",'ok')
        return redirect(url_for("admin.preview_edit",id=id))
    return render_template("admin/preview_edit.html",
                           form = form,preview = preview)

# 14.预告管理-预告删除
@admin.route("/preview_del/<int:id>",methods=['GET','POST'])
def preview_del(id=None):
    # 10.1 查看是否存在该预告
    preview = Preview.query.get_or_404(id)
    # 10.2 删除预告
    if not preview is None:
        # 10.3 删除预告海报
        os.remove(app.config['UP_DIR']+preview.logo)
        # 10.4 删除电影对象
        db.session.delete(preview)
        db.session.commit()
        # 10.5 提示框
        flash(f'电影<<<{preview.title}>>>删除了','ok')
        # 10.6 重定向
        return redirect(url_for("admin.preview_list",page=1))

# 15.会员管理-会员列表
@admin.route("/user_list/<int:page>",methods=['GET'])
def user_list(page=None):
    # 15.1 判断page是否有值
    if page is None:
        page = 1
    # 15.2 根据添加的时间分页数据
    page_data = User.query.order_by(User.addtime.desc())\
                .paginate(page=page,per_page=5)
    # 15.3  返回user_list.html
    return render_template("admin/user_list.html",
                           page_data=page_data)

# 16.会员管理-查看会员
@admin.route("/user_view/<int:id>",methods=['GET'])
def user_view(id=None):
    # 16.1 获取fp参数
    form_page = request.args.get("fp")
    # 16.2 判断fp是否有值
    if not form_page:
        form_page = 1
    # 16.3  根据id值查询会员数据
    user = User.query.get_or_404(int(id))
    return render_template("admin/user_view.html",
                           user=user,form_page=form_page)


# 17.会员管理-删除会员
@admin.route("/user_del/<int:id>",methods=['GET'])
def user_del(id=None):
    # 17.1 删除当前会员
    form_page = int(request.args.get("fp"))-1
    # 17.2 判断如果form_page
    if not form_page:
        form_page = 1
    # 17.3 通过id查询数据
    user = User.query.get_or_404(int(id))
    # 17.4 删除会员
    db.session.delete(user)
    db.session.commit()
    # 17.5 弹出框
    flash("删除会员成功!!!!",'ok')
    return redirect(url_for("admin.user_list",page=form_page))

# 18.评论管理-评论列表
@admin.route("/comment_list/<int:page>",methods=['GET'])
def comment_list(page=None):
    # 18.1 判断page是否为None
    if page is None:
        page = 1
    # 18.2 多表关联查询
    page_data = Comment.query.join(Movie).join(User).filter(
        Movie.id == Comment.movie_id,
        User.id == Comment.user_id
    ).order_by(Comment.addtime.desc())\
        .paginate(page=page,per_page=5)
    # 18.3 返回视图
    return render_template("admin/comment_list.html",
                           page_data=page_data)

# 19.评论管理-删除评论
@admin.route("/comment_del/<int:id>",methods=['GET'])
def comment_del(id=None):
    # 19.1 删除当前页
    # 41 ==>每页10条===>5页===>删除第41条===>4页
    form_page = int(request.args.get('fp'))-1
    # 19.2  判断是否为空
    if not form_page:
        form_page = 1
    # 19.3 通过id查询数据
    comment = Comment.query.get_or_404(int(id))
    # 19.4 删除评论
    db.session.delete(comment)
    db.session.commit()
    # 19.5 弹出框
    flash("删除评论成功了!!!",'ok')
    return redirect(url_for('admin.comment_list',
                            page=form_page))

# 20.收藏管理-收藏列表
@admin.route("/moviecol_list/<int:page>",methods=['GET'])
def moviecol_list(page=None):
    # 20.1 判断page是否为None
    if page is None:
        page = 1
    # 20.2 多表关联查询
    page_data = Moviecol.query.join(Movie).join(User).filter(
        Movie.id == Moviecol.movie_id,
        User.id == Moviecol.user_id
    ).order_by(Moviecol.addtime.desc())\
    .paginate(page=page,per_page=1)
    #  20.3 返回视图
    return render_template("admin/moviecol_list.html",
                           page_data=page_data)

# 21.收藏管理-删除收藏
@admin.route("/moviecol_del/<int:id>",methods=['GET'])
def moviecol_del(id=None):
    # 21.1 删除当前页
    form_page = int(request.args.get('fp'))-1
    # 21.2 判断是否有值
    if  not  form_page:
        form_page = 1
    # 21.3 通过id查询数据
    moviecol = Moviecol.query.get_or_404(int(id))
    # 21.4 删除用户
    db.session.delete(moviecol)
    db.session.commit()
    # 21.5 弹出框
    flash("删除收藏成功!!!!",'ok')
    return redirect(url_for('admin.moviecol_list',
                            page=form_page))


#  22.日志管理-操作日志列表
@admin.route("/oplog_list/<int:page>",methods=['GET'])
def oplog_list(page=None):
    # 22.1 判断page是否为None
    if page is None:
        page = 1
    # 22.2 多表关联查询
    page_data = Oplog.query.join(Admin).filter(
        Admin.id == Oplog.admin_id
    ).order_by(Oplog.addtime)\
    .paginate(page=page,per_page=5)
    return render_template("admin/oplog_list.html",
                           page_data=page_data)
#  23.日志管理-管理员登录日志列表
@admin.route("/adminlog_list/<int:page>",methods=['GET'])
def adminlog_list(page=None):
    # 23.1 判断page是否为None
    if page is None:
        page = 1
    # 23.2 多表关联查询
    page_data = Adminlog.query.join(Admin).filter(
        Admin.id == Adminlog.admin_id
    ).order_by(Adminlog.addtime)\
    .paginate(page=page,per_page=5)
    return render_template("admin/adminlog_list.html",
                           page_data=page_data)
#  24.日志管理-会员登录日志列表
@admin.route("/userlog_list/<int:page>",methods=['GET'])
def userlog_list(page=None):
    # 23.1 判断page是否为None
    if page is None:
        page = 1
    # 23.2 多表关联查询
    page_data = Userlog.query.join(User).filter(
        User.id == Userlog.user_id
    ).order_by(Userlog.addtime)\
    .paginate(page=page,per_page=5)
    return render_template("admin/userlog_list.html",
                           page_data=page_data)

# 25.权限管理-权限添加
@admin.route("/auth_add/",methods=['GET','POST'])
def auth_add():
    # 25.1 获取预告表单
    form = AuthForm()
    # 25.2 判断是否点击按钮
    if form.validate_on_submit():
        # 25.3 获取表单数据
        data = form.data
        # 25.4 设置模型
        auth = Auth(
            name = data['name'],
            url = data['url']
        )
        # 25.5 添加数据
        db.session.add(auth)
        db.session.commit()
        # 25.6 弹出框
        flash("添加权限成功!!!",'ok')
        # 25.7 重定向
        return redirect(url_for("admin.auth_add"))
    return render_template("admin/auth_add.html",form=form)

#  26.权限管理-权限列表
@admin.route("/auth_list/<int:page>",methods=['GET'])
def auth_list(page=None):
    # 26.1 判断page是否为None
    if page is None:
        page = 1
    # 26.2 多表关联查询
    page_data = Auth.query.order_by(Auth.addtime)\
        .paginate(page=page,per_page=2)
    return render_template("admin/auth_list.html",
                           page_data=page_data)

# 27.权限管理-权限编辑
@admin.route("/auth_edit/<int:id>",methods=['GET','POST'])
def auth_edit(id=None):
    # 27.1 获取权限表单
    form = AuthForm()
    # 27.2 根据id查询
    auth = Auth.query.get_or_404(int(id))
    # 27.3 修改form的按钮
    form.submit.label.text ="编辑"
    # 27.4 判断表单提交
    if form.validate_on_submit():
        # 27.5 获取表单数据
        data = form.data
        # 27.6 设置其他数据
        auth.name = data['name']
        auth.url = data['url']
        # 27.7 数据提交
        db.session.add(auth)
        db.session.commit()
        # 27.8 弹出框
        flash("修改权限成功",'ok')
        return redirect(url_for('admin.auth_edit',id=id))
    return render_template('admin/auth_edit.html',form=form,
                           auth=auth)

# 28.权限管理-删除权限
@admin.route("/auth_del/<int:id>",methods=['GET'])
def auth_del(id=None):
    #  28.1 根据id查询标签数据
    auth = Auth.query.filter_by(id=id).first_or_404()
    # 28.2 如果数据库中有该标签则删除
    db.session.delete(auth)
    db.session.commit()
    # 29.3  提示框
    flash("权限删除成功",'ok')
    # 6.4 重定向标签列表页面
    return redirect(url_for('admin.auth_list',page=1))
# 更改文件名称(按照自己的设定的规则设置名称)
def change_filename(filename):
    if "." in filename:
        fileInfo = os.path.splitext(filename)
        newFileName = datetime.now().strftime("%Y%m%d%H%M%S")\
                    +str(uuid.uuid4().hex)+fileInfo[-1]
    else:
        newFileName = datetime.now().strftime("%Y%m%d%H%M%S") \
                      + str(uuid.uuid4().hex) + filename

    return newFileName