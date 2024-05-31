电影管理系统
1.导入数据库
    1.1 movie.sql文件导入到mysql数据库中
2.新建app包
    将 static ,templates放入app包中存放
    2.1 static ===> 存放公共的资源   js/css/jquery/image..
    2.2 templates===> 存储静态文件  html/jsp
    2.3 将app.py删除

3.新建manage.py文件
    3.1 JSNUMovie2024文件夹下文件manage.py
    3.2 manage.py文件代替app.py功能
    3.3 flask_script报错
        cmd ===>pip install flask-script 下载第三方模块

4.app包下 __init__.py 文件添加代码
    下载第三方模块
    cmd ===>pip install flask-sqlalchemy (数据库的驱动功能包)
    cmd ===>pip install flask-redis      (缓存机制的功能包)
    4.1 设置项目名称
    4.2 设置数据库连接
    4.3 设置项目缓存
    4.4 设置DEBUG模式
    4.5 数据库连接
    4.6 设置缓存机制
    4.7 设置蓝图(提高编程效率)

5.app包下 新建admin包
    5.1 admin包下 __init__.py 设置当前模块蓝图的名称
    5.2 admin包下 新建views文件(视图文件)
    5.3 admin包下/views 新建login函数
6.app/templates下 新建admin文件夹
    6.1 app/templates/admin 新建login.html

7.设置修改运行的文件
    7.1 打开右上角播放按键左边  Edit Configuration....
        选择左上角+
        选择Python
        修改Name ===>MovieManager
        添加Parameters ===>runserver
        添加Script path ===>选择JSNUMovie2024文件夹下Manager.py文件 主运行文件
    7.2 点击右上角播放按钮  启动服务器
    7.3 打开控制台 127.0.0.1:5000 打开浏览器
    7.4 输入url 127.0.0.1:5000/admin/login
        查看是否进入login.html
8.app/templates/admin/login.html 修改页面
    8.1 网站资源 复制粘贴到 static文件夹下
    8.2 修改login.html页面
9.admin/views文件中
    9.1 修改login函数
    9.2 在app/admin/ 新建 forms.py文件
        cmd===>pip install flask-wtf==1.0.0

10.app包下新建models.py文件
    10.1 编写Admin类
    10.2 编写Adminlog类

11.补全 views.py文件的login函数
12.views.py中新建index函数
13.templates/admin下新建index.html
14.运行时 出现缺少驱动的问题
    cmd ===>pip install mysql-connector
    如果是8.0数据库
    cmd ===>pip install mysql-connector-python

15. 修改index.html页面
    15.1 头部区域 admin.html
    15.2 主区域显示主页的内容
    15.3 底部区域 js区域
16.新建admin.html并编写
17.新建grid.html 菜单页面
18.标签管理-添加标签
    18.1 grid.html 中添加标签请求
    18.2 views.py添加  tag_add函数
    18.3 forms.py添加  TagForm()
    18.4 admin文件夹中添加 tag_add.html
    18.5 models.py文件中添加  Tag类
19.标签管理-标签列表
    19.1 grid.html中添加标签列表请求
    19.2 views.py中添加 tag_list函数
    19.3 admin文件夹中添加tag_list.html
    19.4 新建ui/admin_page.html(分页页面)

20.标签管理-标签编辑
    20.1 tag_list.html中发送编辑请求
    20.2 views.py中添加 tag_edit函数
    20.3 admin文件夹下添加tag_edit.html
21.标签管理-标签删除
    21.1 tag_list.html 中发送编辑请求
    21.2 views.py中添加tag_del函数

22.电影管理-添加电影和电影列表
    22.1  grid.html中设置电影管理 添加电影和电影列表
    22.2  views.py中添加movie_add和movie_list请求函数
    22.3 forms.py中添加MovieForm
    22.4 models.py中添加Movie函数
        外键关联 Comment评论  MovieCol收藏
        管理员登录 Adminlog函数
    22.5 admin文件夹下  movie_add.html  和movie_list.html

23.电影管理-电影列表
    23.1 grid.html 发送url请求
    23.2 views.py中添加 movie_list函数
    23.3 admin文件夹下 新建 movie_list.html

24.电影管理-电影编辑
    24.1 movie_list.html添加编辑请求
    24.2 views.py中添加函数movie_edit
    24.3 admin文件夹下新建 movie_edit.html

25.电影管理-电影删除
    25.1 movie_list.html添加删除请求
    25.2 views.py中添加函数movie_del
26.预告管理-添加预告
    26.1 grid.html添加预告请求  admin.preview_add
    26.2 views.py 新建preview_add函数
    26.3 models.py新建 Preview模型
    26.4 forms.py 新建PreviewForm表单
    26.5 admin文件夹下新建preview_add.html
27.预告管理-预告列表
    27.1 grid.html添加预告列表请求  admin.preview_list
    27.2 views.py 新建preview_list函数
    27.3 admin文件夹下新建preview_add.html
28.预告管理-预告编辑
    28.1 preview_list.html 中添加admin.preview_edit
    28.2 views.py 中添加preview_edit函数
    28.3 admin文件夹下新建preview_edith.html
29.预告管理-预告删除
    29.1 preview_list.html 中添加admin.preview_del
    28.2 views.py中添加 preview_del函数


30.会员管理-会员列表
    30.1 grid.html 设置会员管理 会员列表  admin.user_list
    30.2 views.py 新建user_list函数
    30.3 models.py新建 User模型
    30.4 forms.py 新建UserForm表单
    30.5 admin文件夹下新建user_list.html
31.会员管理-会员删除
    31.1 user_list.html 中添加admin.user_del
    31.2 views.py中添加 user_del函数
32.会员管理-会员查看
    32.1 user_list.html 中添加admin.user_view
    32.2 views.py 中添加user_view函数
    32.3 admin文件夹下新建user_view.html
33.评论管理-评论列表
    33.1 grid.html 新建评论管理 以及评论列表请求 comment_list
    33.2 model.py新建 Comment类
    33.3 views.py 新建 comment_list函数
    33.4 admin文件夹下新建  comment_list.html
34.评论管理-评论删除
    34.1 comment_list.html 添加评论删除请求  comment_del
    34.2 views.py添加 comment_del函数

35.收藏管理-收藏列表
    35.1 grid.html 新建收藏管理列表  admin.moviecol_list
    35.2 models.py 添加Moviecol类(Movie解开注释)
            movie.id user.id外键关联
    35.3 views.py 添加moviecol_list函数
    35.4 admin文件夹新建moviecol_list.html
        仿照tag_list.html
        编号  电影 用户 收藏时间 操作事项(删除)
36.收藏管理-收藏删除
    36.1 moviecol_list.html 中添加 删除请求  admin.moviecol_del
    36.2 views.py添加 moviecol_del函数

37.日志管理-日志列表
    37.1 grid.html中 新建日志管理  3 操作日志列表  管理员登录日志列表  会员登录日志列表
    37.2 models.py中 编写 Userlog,Adminlog,Oplog
    37.3 views.py中 添加userlog_list,adminlog_list,oplog_list函数
    37.4 admin文件夹中  userlog_list.html  adminlog_list.html oplog_list.html
38.权限管理-添加权限
    38.1 grid.html 添加权限管理 2 权限添加   权限列表
    38.2 models.py 编写 Auth模型
    38.3 forms.py 编写 AUthForm表单
    38.4 views.py 添加auth_add,auth_list,auth_edit,auth_del
    38.5 admin文件夹中 auth_add.html auth_list.html,auth_edit.html


