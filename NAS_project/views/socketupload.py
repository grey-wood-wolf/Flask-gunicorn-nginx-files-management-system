from flask import render_template, request, url_for
from flask.views import MethodView
from config import Dir_path
import os

class SocketUpLoadFile(MethodView):
    def get(self):
        socketupload_status = request.args.get('status')
        store_contents = os.listdir(Dir_path.store_dir)
        return render_template('login.html', store_contents=store_contents, socketupload_status=socketupload_status)

files = {}

def setup_socketupload(socketio):

    """socketio文件处理"""
    # 在 file_upload 事件处理器中
    @socketio.on('file_upload')
    def socketupload(json):
        filename = json['filename']
        filedata = json['data']  # 客户端发送的二进制数据
        file_size = json['size']  # 文件的总大小
        file_id = json['file_id']  # 文件的唯一标识符

        if request.sid not in files:
            receivefile = file(filename, file_size, file_id)
            receivefile.write(filedata)

            if receivefile.nowsize == receivefile.filesize:
                receivefile.temp_save()
                receivefile.save()
                socketio.emit('socketupload', {'url':url_for('socketupload'), 'status':'success'}, room=request.sid)
            else:
                files[request.sid] = receivefile
                socketio.emit('send_again', room=request.sid)
        else:
            receivefile = files[request.sid]
            receivefile.write(filedata)

            if receivefile.nowsize == receivefile.filesize:
                receivefile.temp_save()
                receivefile.save()
                del files[request.sid]
                socketio.emit('socketupload', {'url':url_for('socketupload'), 'status':'success'}, room=request.sid)
            else:
                if len(receivefile.filedata) > 1024 * 1024 * 512:
                    receivefile.temp_save()
                socketio.emit('send_again', room=request.sid)

    
class file:
    def __init__(self, filename, filesize, fileid):
        self.filename = filename
        self.filedata = b''
        self.filesize = filesize
        self.nowsize = 0
        self.fileid = str(fileid)

    def write(self, data):
        self.filedata += data
        self.nowsize += len(data)
    
    def temp_save(self):
        with open(os.path.join(Dir_path.store_dir, self.fileid), 'ab') as file:
            # 光标移动到文件末尾
            file.seek(0, 2)
            file.write(self.filedata)
        self.filedata = b''

    def save(self):
        counter = 1
        while os.path.exists(os.path.join(Dir_path.store_dir, self.filename)):
            name, ext = os.path.splitext(self.filename)
            new_filename = f"{name}_{counter}{ext}"
            self.filename = new_filename
            counter += 1
        
        os.rename(os.path.join(Dir_path.store_dir, self.fileid), os.path.join(Dir_path.store_dir, self.filename))
    