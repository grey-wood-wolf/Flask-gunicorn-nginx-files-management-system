from flask import render_template, request
from flask.views import MethodView
from config import Dir_path
import os

class LoginView(MethodView):
    def get(self):
        store_contents = os.listdir(Dir_path.store_dir)
        return render_template('login.html', store_contents=store_contents)
