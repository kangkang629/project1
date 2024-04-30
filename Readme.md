后台管理帐号：



### 代码结构

- server目录是后端代码
- web目录是前端代码

### 部署运行

#### 后端运行步骤

(1) 安装python 3.8+

(2) 安装依赖。进入server目录下，执行 pip install -r requirements.txt

(3) 安装mysql 5.7数据库，并创建数据库，命名为shop，创建SQL如下：
```
CREATE DATABASE IF NOT EXISTS shop DEFAULT CHARSET utf8 COLLATE utf8_general_ci
```
(4) 恢复shop.sql数据。在mysql下依次执行如下命令：

```
mysql> use shop;
mysql> source D:/xxx/xxx/shop.sql;
```
(5) 在项目->server->settings.py中配置数据库账号和密码
![img.png](img.png)
(6) 启动django服务。在server目录下执行：
```
python manage.py runserver
```

#### 前端运行步骤

(1) 安装node 16.14

(2) 进入web目录下，安装依赖，执行:
```
npm install 
```
(3) 运行项目
```
npm run dev
```


