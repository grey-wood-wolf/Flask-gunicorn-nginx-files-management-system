import eventlet
eventlet.monkey_patch()

from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
import threading


from views.login_view import LoginView
from views.upload import UpLoadFile
from views.download import DownLoadFile
from views.del_file import DelFile
from views.socketupload import SocketUpLoadFile
from views.socketdownload import SocketDownLoadFile
from views.webterminal import WebTerminal_view
from views.socketupload import setup_socketupload
from views.socketdownload import setup_socketdownload
from views.webterminal import setup_webterminal
# ...

# from ftp_server import start_ftp_server

app = Flask(__name__, template_folder='shows')
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, max_http_buffer_size=1024 * 1024, ping_timeout=60, ping_interval=25)

# 添加您现有的路由和视图
app.add_url_rule('/', view_func=LoginView.as_view('login'))
app.add_url_rule('/upload', view_func=UpLoadFile.as_view('upload'))
app.add_url_rule('/download', view_func=DownLoadFile.as_view('download'))
app.add_url_rule('/delfile', view_func=DelFile.as_view('delfile'))
app.add_url_rule('/socketupload', view_func=SocketUpLoadFile.as_view('socketupload'))
app.add_url_rule('/socketdownload', view_func=SocketDownLoadFile.as_view('socketdownload'))
app.add_url_rule('/webterminal', view_func=WebTerminal_view.as_view('webterminal'))
setup_socketupload(socketio)
setup_socketdownload(socketio)
setup_webterminal(socketio)


if __name__ == '__main__':
    # ftp_thread = threading.Thread(target=start_ftp_server)
    # ftp_thread.start()

    socketio.run(app, host='0.0.0.0', port=80)
