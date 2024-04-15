from flask import render_template, request
from flask.views import MethodView
from config import Dir_path
import os

class UpLoadFile(MethodView):
    def post(self):
        try:
            file = request.files['file']
            filename = file.filename
            if filename == '':
                raise Exception('No file selected')
            file_path = os.path.join(Dir_path.store_dir, filename)

            # 检查是否有同名文件,如果有则在文件名后加(1)、(2)等后缀
            counter = 1
            while os.path.exists(file_path):
                name, ext = os.path.splitext(filename)
                new_filename = f"{name}_{counter}{ext}"
                file_path = os.path.join(Dir_path.store_dir, new_filename)
                counter += 1

            file.save(file_path)
            store_contents = os.listdir(Dir_path.store_dir)
            return render_template('login.html', store_contents=store_contents, upload_status='success')
        except:
            store_contents = os.listdir(Dir_path.store_dir)
            return render_template('login.html', store_contents=store_contents, upload_status='error')
    
    def get(self):
        store_contents = os.listdir(Dir_path.store_dir)
        return render_template('login.html', store_contents=store_contents)