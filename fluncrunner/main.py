from webob import Request, Response
from webob.exc import *

import subprocess



class FluncRunner(object):
    """
    runs flunc tests. use like::

    >>> from fluncrunner.main import FluncRunner
    >>> runner = FluncRunner("/path/to/ftests/")
    >>> variables = dict(username='lammy', pw='lammyspw')
    >>> return_code = runner.execute("mysuite", variables)
    >>> if runner.execute("mysuite", variables, search_path="/other/path/"):
    ...    print "test failed. browser dump:"
    ...    print self.error_dump()
    
    it is also a wsgi callable. in that context::

     * environ['PATH_INFO'] is the suite to run
     * request.POST is the variable dict
     * a successful response is 200 OK with an uninteresting response body
     * a failure response is 500 Server Error with the browser dump as response body
    """

    search_path = None

    def __init__(self, search_path):
        self.search_path = search_path  # flunc -p option

    def execute_tests(self, suite, vars, search_path=None):
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

    def error_dump(self):
        """
        return a dump of the browser html after an error 

        exceptions will pass through if this is called at the wrong time.
        """
        # TODO: this should be captured, not saved to filesystem
        fp = open('err.html')
        err = fp.read()
        fp.close()
        return err    

    def __call__(self, environ, start_response):
        req = Request(environ)

        suite = req.path_info.strip('/')
        vars = dict(request.POST)

        ret = self.execute_tests(suite, vars)
        
        if ret:
            err = self.error_dump()
            ret = HTTPServerError()
            ret.body = err
            return ret(environ, start_response)

        return Response("Ok" % ret)(environ, start_response)

def app_factory(global_conf, search_path=None, **kw):
    app = FluncRunner(search_path)

    return app
