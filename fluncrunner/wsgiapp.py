import sampleapp
from paste.deploy.config import ConfigMiddleware

def make_app(global_conf, search_path=None, **kw):
    app = sampleapp.App(search_path)

    return app

