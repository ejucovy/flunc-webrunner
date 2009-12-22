from webob import Request, Response
from webob.exc import *

import subprocess



class FluncRunner(object):

    search_path = None

    def __init__(self, search_path):
        self.search_path = search_path  # flunc -p option

    def execute_tests(self, suite, search_path=None):
        assert ".." not in suite and "/" not in suite

        search_path = search_path or self.search_path

        defines = ''
        for key, val in vars.items():
            if key and val:
                defines += "%s=%s," % (key, val)
        defines = defines.strip(',')

        # now construct the commandline call to flunc
        # XXX TODO: flunc should have an API
        args = ['flunc']
        if search_path:
            args.extend(['-p', self.search_path])
        if defines:
            args.extend(['-D', defines])
        args.append(suite)

        print args

        ret = subprocess.call(args)
        return ret

    def __call__(self, environ, start_response):
        req = Request(environ)

        suite = req.path_info.strip('/')
        vars = dict(request.POST)

        ret = self.execute_tests(suite, vars)
        
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
