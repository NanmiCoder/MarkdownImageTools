import os

def load_style_sheet():
    style_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'styles.qss')
    with open(style_path, 'r') as f:
        return f.read()
