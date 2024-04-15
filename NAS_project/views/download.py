from flask import render_template, send_file, request, make_response
from flask.views import MethodView
from config import Dir_path
import os

class DownLoadFile(MethodView):
    def post(self):
        try:
            filename = request.form.get('filename')
            if filename:
                file_path = os.path.join(Dir_path.store_dir, filename)
                if os.path.exists(file_path):
                    response = make_response(send_file(file_path, as_attachment=True))
                    response.set_cookie('downloadStarted', '1', max_age=60)  # 设置 Cookie 有效期为60秒
                    return response
            raise Exception('No file selected')
        except:
            store_contents = os.listdir(Dir_path.store_dir)
            return render_template('login.html', store_contents=store_contents, download_status='error')
    
    def get(self):
        store_contents = os.listdir(Dir_path.store_dir)
        return render_template('login.html', store_contents=store_contents)