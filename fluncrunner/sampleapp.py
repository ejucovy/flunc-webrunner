from webob import Request, Response
from webob.exc import *

import subprocess

class App(object):

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
            args.extend('-D', defines)

        args.append(suite)

        ret = subprocess.call(args)
        
        if ret:
            fp = open('err.html')
            err = fp.read()
            fp.close()
            ret = HTTPServerError()
            ret.body = err
            return ret(environ, start_response)

        return Response("Ok" % ret)(environ, start_response)

def composite_factory(loader, global_conf, **local_conf):
    get = loader.get_app(local_conf['get'])
    post = loader.get_app(local_conf['post'])
    return MethodDispatcher(get, post)
    
class MethodDispatcher(object):
    def __init__(self, get, post):
        self.get = get
        self.post = post

    def __call__(self, environ, start_response):
        method = environ['REQUEST_METHOD']
        if method == "GET":
            return self.get(environ, start_response)
        if method == "POST":
            return self.post(environ, start_response)

        return HTTPMethodNotAllowed()(environ, start_response)
