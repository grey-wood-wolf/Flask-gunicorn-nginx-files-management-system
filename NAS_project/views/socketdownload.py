from flask import render_template, request, url_for
from flask.views import MethodView
from config import Dir_path
import os

class SocketDownLoadFile(MethodView):
    def get(self):
        socketdownload_status = request.args.get('status')
        store_contents = os.listdir(Dir_path.store_dir)
        return render_template('login.html', store_contents=store_contents, socketdownload_status=socketdownload_status)
    

files = {}

def setup_socketdownload(socketio):

    """socketio文件处理"""
    # 在 file_upload 事件处理器中
    @socketio.on('file_download')
    def socketdownload(data):
        if request.sid not in files:
            filename = data['filename']
            file_path = os.path.join(Dir_path.store_dir, filename)
            if os.path.exists(file_path):
                # 分成 512 * 1024 字节的块进行发送，传递到socket.on('receive', function(data)中
                sendfile = file(filename)
                data = sendfile.read(512 * 1024)
                if data:
                    all_read = True if sendfile.read_size == sendfile.file_size else False
                    socketio.emit('receive', \
                                  {'data': data, \
                                    'url':url_for('socketdownload'), \
                                    'filesize': sendfile.file_size, \
                                    'readsize': sendfile.read_size, \
                                    'all_read': all_read}, \
                                    room=request.sid)
                    if all_read:
                        sendfile.close()
                    else:
                        files[request.sid] = sendfile
            else:
                print('文件不存在')
        else:
            sendfile = files[request.sid]
            data = sendfile.read(512 * 1024)
            if data:
                all_read = True if sendfile.read_size == sendfile.file_size else False
                socketio.emit('receive', \
                              {'data': data, \
                                'url':url_for('socketdownload'), \
                                'filesize': sendfile.file_size, \
                                'readsize': sendfile.read_size, \
                                'all_read': all_read}, \
                                room=request.sid)
                if all_read:
                    sendfile.close()
                    del files[request.sid]
            else:
                files[request.sid] = sendfile
    

class file:
    def __init__(self, filename):
        self.filename = filename
        self.file_path = os.path.join(Dir_path.store_dir, filename)
        self.file_size = os.path.getsize(self.file_path)
        self.file = open(self.file_path, 'rb')
        self.read_size = 0

    def read(self, size):
        data = self.file.read(size)
        self.read_size += len(data)
        return data

    def close(self):
        self.file.close()