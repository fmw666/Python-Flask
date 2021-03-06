# 导入模块
import tornado.ioloop
import tornado.web

from pymysql import connect
import json

# 创建视图类
class MainHandler(tornado.web.RequestHandler):
    
    # 请求方式：get、post、put、delete

    # 导入 html 方式1：读取文件
    # def get(self):
    #     # 打开文件返回
    #     with open('./templates/index.html', 'rb') as f:
    #         content = f.read()
    #     self.write(content)
    
    # 导入 html 方式2：专门用来显示模板内容的方法
    def get(self):
        # 读取数据库数据，传入给模板页面用以渲染

        # 1. 连接数据库
        conn = connect(host='localhost', port=3306, database='book_manager', user='root', password='fmw19990718', charset='utf8')

        # 获得 Cursor 对象
        cs1 = conn.cursor()

        # 2. 执行查询的 sql 语句
        cs1.execute("select * from books;")
        # 得到返回的数据
        data = cs1.fetchall()

        # 3. 关闭数据库连接
        cs1.close()
        conn.close()

        # 传入模板页面
        self.render('index.html', show_list=data)

    def post(self):
        # 得到前端的数据，再插入到数据库

        # 1. 创建一个列表用以接收前端数据
        params_list = list()
        params_list.append(self.get_argument('btitle'))
        params_list.append(self.get_argument('bauthor'))
        params_list.append(self.get_argument('bperson'))
        params_list.append(self.get_argument('bpub_date'))
        params_list.append(self.get_argument('bread'))
        params_list.append(self.get_argument('bcomment'))

        # 2. 连接数据库，进行插入
        conn = connect(host='localhost', port=3306, database='book_manager', user='root', password='fmw19990718', charset='utf8')
        cs1 = conn.cursor()
        cs1.execute("insert into books(btitle, bauthor, bperson, bpub_date, bread, bcomment) values (%s, %s, %s, %s, %s, %s)", params_list)
        # 提交数据
        conn.commit()
        # 关闭连接
        cs1.close()
        conn.close()

        # 3. 返回一个 json 格式的数据，或直接返回一个字典
        self.write({'data': '添加成功'})

    def put(self):

        # 1. 得到前端传过来的 body 数据
        params_list = list()
        params_list.append(self.get_argument('btitle'))
        params_list.append(self.get_argument('bauthor'))
        params_list.append(self.get_argument('bperson'))
        params_list.append(self.get_argument('bpub_date'))
        params_list.append(self.get_argument('bread'))
        params_list.append(self.get_argument('bcomment'))
        params_list.append(self.get_argument('bid'))

        # 2. 连接数据库
        conn = connect(host='localhost', port=3306, database='book_manager', user='root', password='fmw19990718', charset='utf8')
        cs1 = conn.cursor()

        # 3. 执行 sql 更新语句
        cs1.execute("update books set btitle=%s, bauthor=%s, bperson=%s, bpub_date=%s, bread=%s, bcomment=%s where id = %s", params_list)
        # 提交
        conn.commit()
        # 关闭连接
        cs1.close()
        conn.close()

        # 5. 返回对应的数据
        self.write({"data": "更新成功"})

    def delete(self):

        # 1. 得到前端的数据 并 解码
        decode_body = self.request.body.decode('utf-8')

        # 2. 转成字典
        params_dict = json.loads(decode_body)

        # 3. 连接数据库
        conn = connect(host='localhost', port=3306, database='book_manager', user='root', password='fmw19990718', charset='utf8')
        cs1 = conn.cursor()

        # 4. 执行 sql 更新语句
        cs1.execute("delete from books where id = %(id)s", params_dict)
        # 提交
        conn.commit()
        # 关闭连接
        cs1.close()
        conn.close()

        # 5. 返回对应的数据
        self.write({"data": "删除成功"})

# 程序配置
def make_app():
    # 路由配置
    return tornado.web.Application([
        (r"/", MainHandler),
    ],
        static_path = './static',   # 静态文件夹路径
        template_path = './templates'   # 模板路径
    )


# 程序入口
if __name__ == "__main__":
    # 加载配置
    app = make_app()
    # 设置监听
    app.listen(8888)
    # 开启服务(ioloop 实际上是对 epoll 的封装)
    tornado.ioloop.IOLoop.current().start()
