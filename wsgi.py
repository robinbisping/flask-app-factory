import sys
from os import path

app_root = path.abspath(path.join(path.dirname(__file__), "neon"))

if app_root not in sys.path:
    sys.path.insert(0, app_root)


from neon.app import create_app
app = create_app()
app.run()
