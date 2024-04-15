import os

class Dir_path:
    root_dir = os.path.dirname(os.path.abspath(__file__))
    view_dir = f'{root_dir}/views/'
    store_dir = f'{root_dir}/store/'