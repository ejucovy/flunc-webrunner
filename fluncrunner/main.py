from webob import Request, Response
from webob.exc import *

import subprocess

class FluncRunner(object):

    def __init__(self, search_path):
        self.search_path = search_path  # flunc -p option

    def __call__(self, environ, start_response):
        req = Request(environ)

        suite = req.path_info.strip('/')
        assert ".." not in suite and "/" not in suite

        defines = ''
        for key, val in dict(req.POST).items():
            defines = "%s=%s," % (key, val)
        defines = defines.strip(',')

        args = ['flunc']
        if self.search_path:
            args.extend(['-p', self.search_path])
        if defines:
            args.extend(['-D', defines])

        args.append(suite)

        ret = subprocess.call(args)
        
        if ret:
            # TODO: this should be captured, not saved to filesystem
            fp = open('err.html')
            err = fp.read()
            fp.close()
            ret = HTTPServerError()
            ret.body = err
            return ret(environ, start_response)

        return Response("Ok" % ret)(environ, start_response)

def app_factory(global_conf, search_path=None, **kw):
    app = FluncRunner(search_path)

    return app
