## flask 教程

&emsp;&emsp;简介：flask 是一款非常流行的 Python Web 框架，出生于 2010 年，作者是 Armin Ronacher。本来这个项目只是作者在愚人节的一个玩笑，后来由于非常受欢迎，进而成为一个正式的项目。

&emsp;&emsp;flask 自 2010 年发布第一个版本以来，大受欢迎，深得开发者的喜爱，并且在多个公司已经得到了应用，flask 能如此流行的原因，可以分为以下几点：

+ 微框架、简洁，只做他需要做的，给开发提供了很大的扩展性。
+ flask 和相关的依赖（Jinja2、Werkzeug）设计得非常优秀，用起来很爽。
+ 开发效率非常高，比如使用 SQLAlchemy 的 ORM 操作数据库可以节省开发者大量书写 sql 的时间。
+ 社会活跃度非常高，保证了一个良好的生态。

> 中文文档：[http://docs.jinkan.org/docs/flask/](http://docs.jinkan.org/docs/flask/)

1. **[安装 flask](#-安装-flask)**

1. **[连接数据库](#-连接数据库)**

1. **[项目搭建](#-项目搭建)**

1. **[模板语言](#-模板语言)**

1. **[分页实现](#-分页实现)**

1. **[扩展插件](#-扩展插件)**

1. **[实现增删改查](#-实现增删改查)**

---

### 🔨 安装 flask

+ 执行 pip 模块下载命令：

    ```python
    pip install flask
    ```

+ 查看当前 flask 版本：

    ```python
    import flask

    print(flask.__version__)
    ```

+ 官方示例的一段简单的 flask Web 应用：

    ```python
    # 导入模块
    from flask import Flask

    # 构造 app 对象
    app = Flask(__name__)

    # 路由定义（装饰器方式）
    @app.route('/')
    def hello_world():
        return 'Hello World!'

    if __name__ == '__main__':
        # app.run(debug=True)   # 开发模式中开启 debug，默认为未开启
        app.run()
    ```

    > 代码用 Python 解释器来运行。注意：确保你的应用文件名不是 flask.py ，因为这将与 Flask 本身冲突。本示例此脚本名均为 **app.py**

### 🛢 连接数据库

> 这里以 MySQL 数据库为例。关于 Python 如何操纵数据库，[详情]()

+ 下载 Flask ORM 模块 `SQLAlchemy`：

    ```python
    pip install Flask-SQLAlchemy
    ```

+ 下载 Python 第三方 MySQL 模块 `mysqlclient`：

    ```python
    pip install mysqlclient
    ```

+ 预先创建 MySQL 数据库

    ```sql
    -- 创建数据库
    create database net_news charset=utf8mb4;
    ```

+ 在 flask 项目中配置数据库

    ```python
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost:3306/net_news?charset=utf8'
    db = SQLAlchemy(app)

    class News(db.Model):
        __tablename__ = 'news'
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(200), nullable=False)
        content = db.Column(db.String(2000), nullable=False)
        types = db.Column(db.String(10), nullable=False)
        image = db.Column(db.String(300), )
        author = db.Column(db.String(20), )
        view_count = db.Column(db.Integer)
        created_at = db.Column(db.DateTime)
        is_valid = db.Column(db.Boolean)

        def __repr__(self):
            return '<News %r>' % self.title
    ```

+ 生成数据库表命令：

    ```python
    from app import db

    db.create_all()
    ```

+ 插入数据库表命令：

    ```python
    from app import News
    from app import db

    new_obj = News(
        title = '标题',
        content = '内容',
        types = '推荐',
    )

    db.session.add(new_obj)
    db.session.commit()
    ```

+ 查询数据库表命令：

    ```python
    from app import News

    news_all = News.query.all()
    news_list1 = News.query.filter_by(is_valid=1)
    news_list2 = News.query.filter(News.types=='推荐')
    news_obj = News.query.get(pk=1)
    ```

### ⚙ 项目搭建

+ 项目结构（`*` 代表可选）

    ```bash
    ├── 项目文件夹
    │   ├── app.py          # 程序运行主入口
    │   ├── *models.py      # ORM 数据库生成
    │   ├── *forms.py       # 模板表单生成
    │   ├── *config.py      # 配置文件
    │   ├── db.sql          # 数据库文件
    │   ├── static          # 静态文件存放文件夹
    │   │   ├── css
    │   │   ├── js
    │   │   ├── ..
    │   ├── templates       # 模板页面存放文件夹
    │   │   ├── index.html
    │   │   ├── ..
    ```

+ 我们整篇教程将以一个 **新闻前台展示** 和 **后台数据管理** 项目为例

    ```bash
    ├── 项目文件夹
    │   ├── app.py              # 程序运行主入口
    │   ├── forms.py            # 前端表单数据获取
    │   ├── static              # 静态文件存放文件夹
    │   │   ├── css
    │   │   ├── js
    │   │   ├── ..
    │   ├── templates           # 模板页面存放文件夹
    │   │   ├── admin
    │   │   │   ├── add.html
    │   │   │   ├── admin_base.html
    │   │   │   ├── index.html
    │   │   │   ├── update.html
    │   │   ├── base.html
    │   │   ├── cat.html
    │   │   ├── detail.html
    │   │   ├── index.html
    ```

    > 本章 demo，[访问](project)

### 📝 模板语言

+ 变量

    ***`app.py`：** 后台传值*

    ```python
    @app.route('/cat/')
    @app.route('/cat/<name>/')
    def cat(name=None):
        # 新闻类别，查询类别为 name 的新闻数据
        news_list = News.query.filter(News.types==name)
        return render_template('cat.html', name=name, news_list=news_list)
    ```

    ***`cat.html`：** 模板变量*

    ```html
    <h3>新闻类别：{{ name }}</h3>

    {% for news in news_list %}
    <div>
        <div>
            <img src="{{ news.image }}" alt="图片">
        </div>
        <div class="right-content">
            <h3><a href="{{ url_for('detail', pk=news.id) }}">{{ news.title }}</a></h3>
            <small>{{ news.created_at }}</small>
        </div>
    </div>
    {% endfor %}
    ```

    *引用静态文件* 和 *url 跳转*

    ```html
    {# 引用静态文件 #}

    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css', _external=True) }}">


    {# url 跳转 #}

    <a href="{{ url_for('index', param='参数值') }}">点击跳转</a>
    ```

+ 标签

    ```html
    {# for 循环 #}

    {% for item in items %}
        {{ item.attr }}
    {% endfor %}


    {# if 条件判断 #}

    {% if item == "1" %}
        <span>yes</span>
    {% else %}
        <span>no</span>
    {% endif %}


    {# 继承 #}
    {% extends 'base.html' %}


    {# 插槽 #}

    {% block content %}
    {% endblock %}
    ```

### ✂ 分页实现

+ 后台：

    ```python
    @app.route('/admin/<int:page>/')
    def admin(page=None):
        # 新闻后台管理首页
        if page is None:
            page = 1
        news_list = News.query.paginate(page=page, per_page=5)
        return render_template('admin/index.html', news_list=news_list)
    ```

+ 前端（引入了 bootstrap）：

    ```html
    <nav aria-label="Page navigation">
        <ul class="pagination">
            <li>
                {% if news_list.has_prev %}
                <a href="#" aria-label="Previous">
                    <span aria-hidden="true">&laquo;</span>
                </a>
                {% endif %}
            </li>
            {% for page in news_list.iter_pages() %}
            <li><a href="{{ url_for('admin', page=page) }}">{{ page }}</a></li>
            {% endfor %}
            <li>
                <a href="#" aria-label="Next">
                    <span aria-hidden="true">&raquo;</span>
                </a>
            </li>
        </ul>
    </nav>
    ```

### 🔌 扩展插件

+ 部分插件项目教程：<http://www.pythondoc.com/>

    > 后以 Flask-WTF 这个表单插件为例

+ 介绍

    &emsp;&emsp;使用Flask-WTF，可以在Python脚本中定义表单域并使用HTML模板来呈现它们。

+ 安装

    ```python
    pip install Flask-WTF
    ```

    > GitHub：<https://github.com/lepture/flask-wtf>

+ `forms.py`

    ```python
    #coding=utf-8

    from flask_wtf import FlaskForm
    from wtforms import StringField, TextAreaField, SubmitField, SelectField, RadioField
    from wtforms.validators import DataRequired


    class NewsForm(FlaskForm):
        # 新闻表单
        title = StringField(label='新闻标题', validators=[DataRequired('请输入标题')], 
            description='请输入标题', 
            render_kw={'required': 'required', 'class': 'form-control'})
        content = TextAreaField(label='新闻内容', validators=[DataRequired('请输入内容')], 
            description='请输入内容', 
            render_kw={'required': 'required', 'class': 'form-control'})
        types = SelectField('新闻类型', 
            choices=[('推荐', '推荐'), ('百家', '百家'), ('本地', '本地'), ('图片', '图片')])
        image = StringField(label='新闻图片', 
            description='请输入图片地址', 
            render_kw={'required': 'required', 'class': 'form-control'})
        submit = SubmitField('提交')
    ```

+ `app.py`

    ```python
    ...
    from flask import Flask, render_template, redirect, url_for
    from forms import NewsForm
    from datetime import datetime

    app.config['SECRET_KEY'] = 'a random string'
    ...

    @app.route('/admin/add/', methods=('GET', 'POST'))
    def add():
        # 新闻后台数据新增
        form = NewsForm()
        if form.validate_on_submit():
            # 获取数据
            new_obj = News(
                title = form.title.data,
                content = form.content.data,
                types = form.types.data,
                image = form.image.data,
                created_at = datetime.now(),
                is_valid = True
            )
            # 保存数据
            db.session.add(new_obj)
            db.session.commit()
            return redirect(url_for('admin'))
        return render_template('admin/add.html', form=form)
    ```

### 🔍 实现增删改查

+ 增

    `app.py`

    ```python
    @app.route('/admin/add/', methods=('GET', 'POST'))
    def add():
        # 新闻后台数据新增
        form = NewsForm()
        if form.validate_on_submit():
            # 获取数据
            new_obj = News(
                title = form.title.data,
                content = form.content.data,
                types = form.types.data,
                image = form.image.data,
                created_at = datetime.now(),
                is_valid = True
            )
            # 保存数据
            db.session.add(new_obj)
            db.session.commit()
            return redirect(url_for('admin'))
        return render_template('admin/add.html', form=form)
    ```

    `add.html`

    ```html
    <form class="form-horizontal" role="form" method="post">
        <div class="form-group">
            <label for="inputEmail3" class="col-sm-2 control-label">
                {{ form.title.label.text }}
            </label>
            <div class="col-sm-10">
                {{ form.title }}
            </div>
        </div>

        <div class="form-group">
            <label for="inputPassword3" class="col-sm-2 control-label">
                {{ form.content.label.text }}
            </label>
            <div class="col-sm-10">
                {{ form.content }}
            </div>
        </div>

        <div class="form-group">
            <label for="inputPassword3" class="col-sm-2 control-label">
                {{ form.types.label.text }}
            </label>
            <div class="col-sm-10">
                {{ form.types }}
            </div>
        </div>

        <div class="form-group">
            <label for="inputPassword3" class="col-sm-2 control-label">
                {{ form.image.label.text }}
            </label>
            <div class="col-sm-10">
                {{ form.image }}
            </div>
        </div>

        <div class="form-group">
            <div class="col-sm-offset-2 col-sm-10">
                {{ form.csrf_token }}
                {{ form.submit }}
            </div>
        </div>
    </form>
    ```

+ 删

    `app.py`

    ```python
    @app.route('/admin/delete/<int:pk>/', methods=('GET', 'POST'))
    def delete(pk):
        # 新闻后台数据删除
        news_obj = News.query.get(pk)
        if not news_obj:
            return 'no'
        news_obj.is_valid = False
        db.session.add(news_obj)
        db.session.commit()
        return 'yes'
    ```

    `index.html`

    ```html
    <a class="btn btn-danger" href="javascript:;" data-url="{{ url_for('delete', pk=news_obj.id) }}">删除</a>

    <script>
        $(function() {
            $('.btn-danger').on('click', function() {
                var btn = $(this);
                if(confirm('确定删除该记录吗？')) {
                    $.post(btn.attr('data-url'), function(data) {
                        if(data === 'yes') {
                            btn.parents('tr').hide();
                        } else {
                            alert('删除失败');
                        }
                    })
                }
            })
        })
    </script>
    ```

+ 改

    `app.py`

    ```python
    @app.route('/admin/update/<int:pk>/', methods=('GET', 'POST'))
    def update(pk):
        # 新闻后台数据修改
        news_obj = News.query.get(pk)
        # 如果没有数据，则返回
        if not news_obj:
            return redirect(url_for('admin'))
        form = NewsForm(obj=news_obj)
        if form.validate_on_submit():
            # 获取数据
            news_obj.title = form.title.data
            news_obj.content = form.content.data
            # 保存数据
            db.session.add(news_obj)
            db.session.commit()
            return redirect(url_for('admin'))
        return render_template('admin/update.html', form=form)
    ```

    `index.html`

    ```html
    <a class="btn btn-info" href="{{ url_for('update', pk=news_obj.id) }}">修改</a>
    ```

    `update.html`

    ```html
    <form class="form-horizontal" role="form" method="post">
        <div class="form-group">
            <label for="inputEmail3" class="col-sm-2 control-label">
                {{ form.title.label.text }}
            </label>
            <div class="col-sm-10">
                {{ form.title }}
            </div>
        </div>

        <div class="form-group">
            <label for="inputPassword3" class="col-sm-2 control-label">
                {{ form.content.label.text }}
            </label>
            <div class="col-sm-10">
                {{ form.content }}
            </div>
        </div>

        <div class="form-group">
            <label for="inputPassword3" class="col-sm-2 control-label">
                {{ form.types.label.text }}
            </label>
            <div class="col-sm-10">
                {{ form.types }}
            </div>
        </div>

        <div class="form-group">
            <label for="inputPassword3" class="col-sm-2 control-label">
                {{ form.image.label.text }}
            </label>
            <div class="col-sm-10">
                {{ form.image }}
            </div>
        </div>

        <div class="form-group">
            <div class="col-sm-offset-2 col-sm-10">
                {{ form.csrf_token }}
                {{ form.submit }}
            </div>
        </div>
    </form>
    ```

+ 查

    `app.py`

    ```python
    @app.route('/admin/')
    @app.route('/admin/<int:page>/')
    def admin(page=None):
        # 新闻后台管理首页
        if page is None:
            page = 1
        news_list = News.query.filter_by(is_valid=True).paginate(page=page, per_page=5)
        return render_template('admin/index.html', news_list=news_list)
    ```

    `index.html`

    ```html
    <table class="table table-striped">
        <thead>
            <tr>
                <th>编号</th>
                <th>新闻标题</th>
                <th>类别</th>
                <th>添加时间</th>
                <th>操作</th>
            </tr>
        </thead>
        <tbody>
            {% for news_obj in news_list.items %}
            <tr>
                <td>{{ news_obj.id }}</td>
                <td>{{ news_obj.title }}</td>
                <td>{{ news_obj.types }}</td>
                <td>{{ news_obj.created_at }}</td>
                <td>
                    <a class="btn btn-info" href="{{ url_for('update', pk=news_obj.id) }}">修改</a>
                    <a class="btn btn-danger" href="javascript:;" data-url="{{ url_for('delete', pk=news_obj.id) }}">删除</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    ```

**[⤴ get to top](#flask-教程)**