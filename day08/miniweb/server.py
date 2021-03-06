import socket
import re
import sys
import multiprocessing


class WSGIServer(object):
    """定义WSGI类"""

    def __init__(self, port, documents_root, app):
        # 1.创建tcp的套接字
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 2.绑定本地信息
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(("", port))
        # 3. 将套接字变为监听套接字
        self.server_socket.listen(128)

        # 设定html资源所在的路径
        self.documents_root = documents_root

        # 设定需要调用的web框架的函数（对象）
        self.app = app

    def run_forever(self):
        """一直运行，等待浏览器的链接，然后为浏览器服务"""

        while True:
            # 4. 等待新用户
            new_socket, new_addr =  self.server_socket.accept()
            new_process = multiprocessing.Process(target=self.deal_with_request, args=(new_socket,))
            new_process.start()
            new_socket.close()


    def deal_with_request(self, new_socket):
        """用一个进程来完成对这个新浏览器客户端的服务"""

        while True:
            # 5. 接收浏览器的请求
            request = new_socket.recv(1024).decode('utf-8')
            # print(request)
            if not request:
                new_socket.close()
                return

            request_lines = request.splitlines()
            for i, line in enumerate(request_lines):
                print(i, line)

            # GET /login.html HTTP/1.1
            ret = re.match(r"([^/]*)([^ ]*)", request_lines[0])
            if ret:
                print("正则处理的数据：", ret.group(1))
                print("正则处理的数据：", ret.group(2))
                # 提取需要的文件名(包含路径)
                file_name = ret.group(2)
                if file_name == "/":
                    file_name = "/index.html"

                # 检查是否含地址栏参数"?code=000056&info=备注文字"
                if '?' in file_name:
                    url_arr = file_name.split('?')
                    file_name = url_arr[0]
                    url_dat = url_arr[1]
                   
                else:
                    url_dat = ''

            
            # 如果后缀不是'_data'结尾，那么就认为是普通的文件，直接读取返回
            # 如果是'_data'结尾，那么就传递给web框架让它处理
            if not file_name.endswith("_data"):
                try:
                    f = open(self.documents_root + file_name, "rb")
                except:
                    response_body = "sorry, 么有你要找的文件...."

                    response_header = "HTTP/1.1 404 Not Found\r\n"
                    response_header += "content-type:text/html; charset=utf-8\r\n"
                    response_header += "Content-Length: %d\r\n" % len(response_body)
                    response_header += "\r\n"

                    response = response_header + response_body

                    new_socket.send(response.encode("utf-8"))
                else:
                    content = f.read()
                    f.close()

                    response_body = content

                    response_header = "HTTP/1.1 200 OK\r\n"
                    response_header += "Content-Length: %d\r\n" % len(response_body)
                    response_header += "\r\n"

                    new_socket.send(response_header.encode("utf-8")+response_body)            
            else:
                # 存储将来给web框架的数据
                env = dict()
                env['PATH_INFO'] = file_name
                env['URL_DAT'] = url_dat

                # 调用web框架中指定的函数
                response_body = self.app(env, self.set_response_headers)

                # 将header和body进行组装
                response_header = "HTTP/1.1 %s\r\n" % self.headers[0]
                for header_temp in self.headers[1]:
                    response_header += "%s:%s\r\n" % (header_temp[0], header_temp[1])
                response_header += "Content-Length:%d\r\n" % (len(response_body.encode("utf-8")))
                response_header += "\r\n"

                response = response_header + response_body

                # 将数据返回给浏览器
                new_socket.send(response.encode("utf-8"))


    def set_response_headers(self, status, headers):
        """设定返回的头信息"""
        # status------>"200 OK"
        # headers----->[("Content-Type", "text/html")]
        # ["200 OK", [("Content-Type", "text/html")]]
        self.headers = [status, headers]


g_static_root = "./static"
g_dynamic_root = "/"


def main():
    """负责控制整体"""
    # python3 web_server.py 7890 my_web:app
    if len(sys.argv) == 3:
        port = sys.argv[1]
        if port.isdigit():
            port = int(port)
        else:
            print("端口号输入错误")
            return

        # 获取web框架中的模块名以及将来需要调用的函数(对象)名
        # my_web:app
        web_frame_app_name = sys.argv[2]
    else:
        print("请以下面方式运行:python3 xxx.py 7890 my_web:app")
        return

    print("web服务器使用的端口是：%d" % port)

    # my_web:app
    ret = re.match(r"([^:]+):(.*)", web_frame_app_name)
    if ret:
        frame_name = ret.group(1)
        app_name = ret.group(2)


    # print(frame_name)
    # print(app_name)
    # return
    
    # 将存放web框架的文件夹 添加到path路径中，这样保证了 导入web框架中的模块没有问题
    sys.path.append(g_dynamic_root)

    frame = __import__(frame_name)
    app = getattr(frame, app_name)

    # print(app)
    # return

    http_server = WSGIServer(port, g_static_root, app)
    http_server.run_forever()


if __name__ == "__main__":
    main()

