# 环境配置
1. 安装Python 3.5.3
2. 安装Django 1.10.7  `pip install django==1.10.7`
3. 安装virtualenv  `pip install virtualenv`
4. 前端框架Bootstrap和Jquery

```
virtualenv env
env\Scripts\activate
python manage.py migrate
python manage.py runserver
```

# 注意事项

如果Model发生变更，执行以下命令

```
python manage.py makemigrations
python manage.py migrate
```

# 后端规则
1. PEP8代码规范
2. 模板存放于`/templates`文件夹中

# 前端规范
1. 静态文件存放于`/static`文件夹中, 基本规则如下：

```
static
    src
    css
    javascrip
    img
```
