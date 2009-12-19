from webob import Request, Response
from webob.exc import *

def App(object):

    def __init__(self, search_path):
        self.search_path = search_path  # flunc -p option

    def __call__(self, environ, start_response):
        req = Request(environ)

        if req.method != "POST":
            return HttpMethodNotAllowed()(environ, start_response)

        defines = ''
        for key, val in dict(req.POST).items():
            defines = "%s=%s," % (key, val)
        defines = defines.strip(',')

        
