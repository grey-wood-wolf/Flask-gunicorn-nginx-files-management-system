from flask import render_template, request
from flask.views import MethodView
import os
import select
import pty

class WebTerminal_view(MethodView):    
    def get(self):
        return render_template('webterminal.html')
    
WebTerminals = {}
def setup_webterminal(socketio):
    """"终端处理"""

    class WebTerminal:
        def __init__(self, sid):
            self.master_fd, self.slave_fd = pty.openpty()
            self.sid = sid
            self.shell = '/bin/bash'
        
        def spawn_shell(self):
            # 启动 shell 进程
            pid = os.fork()
            if pid == 0:  # 子进程
                os.setsid()  # 创建一个新的会话
                os.dup2(self.slave_fd, 0)  # stdin
                os.dup2(self.slave_fd, 1)  # stdout
                os.dup2(self.slave_fd, 2)  # stderr

                # 关闭不需要的文件描述符
                os.close(self.master_fd)
                os.close(self.slave_fd)

                # 执行 shell
                os.execv(self.shell, [self.shell])
            else:  # 父进程
                # 关闭从设备，因为父进程中不需要
                os.close(self.slave_fd)

        def read_terminal(self):
            while True:
                r, w, x = select.select([self.master_fd], [], [], 0.1) 
                if r:
                    output = os.read(self.master_fd, 1024)
                    socketio.emit('terminal_output', {'output': output.decode()}, room=self.sid)

        def terminal_message(self, message):
            os.write(self.master_fd, message['input'].encode())

        def run(self):
            self.spawn_shell()
            # 使用 Flask-SocketIO 的 start_background_task 方法启动后台任务
            socketio.start_background_task(target=self.read_terminal)

    @socketio.on('terminal_init')
    def terminal_init():
        terminal = WebTerminal(request.sid)
        terminal.run()
        WebTerminals[request.sid] = terminal

    @socketio.on('terminal_input')
    def terminal_input(message):
        terminal = WebTerminals[request.sid]
        terminal.terminal_message(message)
