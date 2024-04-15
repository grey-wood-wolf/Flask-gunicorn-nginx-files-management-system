from flask import render_template, request
from flask.views import MethodView
from config import Dir_path
import os

class DelFile(MethodView):
    def post(self):
        try:
            filename = request.form.get('filename')
            if filename:
                file_path = os.path.join(Dir_path.store_dir, filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
                    store_contents = os.listdir(Dir_path.store_dir)
                    return render_template('login.html', store_contents=store_contents, del_status='success')
            raise Exception('No file selected')
        except:
            store_contents = os.listdir(Dir_path.store_dir)
            return render_template('login.html', store_contents=store_contents, del_status='error')
    
    def get(self):
        store_contents = os.listdir(Dir_path.store_dir)
        return render_template('login.html', store_contents=store_contents)