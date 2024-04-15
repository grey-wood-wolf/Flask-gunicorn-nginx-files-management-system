from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from config import Dir_path

def start_ftp_server():
    # 实例化一个虚拟用户授权器
    authorizer = DummyAuthorizer()

    # 添加一个用户权限，参数是用户名、密码、目录和权限
    authorizer.add_user("lzl", "123", Dir_path.store_dir, perm="elradfmw")

    # 初始化FTP处理程序
    handler = FTPHandler
    handler.authorizer = authorizer

    # 创建FTP服务器实例，监听0.0.0.0:21地址和端口
    server = FTPServer(("0.0.0.0", 21), handler)

    # 在新线程中启动FTP服务器
    server.serve_forever()
    