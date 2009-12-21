flunc-webrunner runs flunc tests (suites of twill scripts with variables) through the web.

The API
=======

There is a web API for running a flunc test.

Executing a test
----------------

To execute a test, POST to the test's execution URI.

To execute a test with global variable overrides, provide a www-form-urlencoded 
set of key=value pairs in the request body.

 For example::

POST /basic_test/ HTTP/1.1
Content-Type: application/x-www-form-urlencoded
    username=lammy&password=testy&name_of_friend=bob

 will execute a command like::

flunc -D username=lammy,password=testy,name_of_friend=bob basic_test

Inspecting a test
-----------------

To discover the available variables in a test, GET the test's inspection URI.

An HTML form will be returned, suitable for POSTing back to the server.

If available, default values (from the test's corresponding .conf) will be
detailed in the form fields' pre-filled values.

Configuring the server
======================

The flunc-webrunner server uses Paste Deploy for configuration.

A sample configuration, suitable for forking, can be found in

 /docs/devel_config.ini

An app_factory is provided. It implements the test execution API
and requires one piece of configuration: a filesystem path that
points to a directory of flunc tests that may be run. This is
equivalent to flunc's -p option on the command line::

 [app:flunc]
 use = egg:fluncrunner
 search_path = %(here)s/ftests/

You will want to configure this app to respond to POST requests.
A composite_factory `request_method` is provided which will
dispatch requests to applications based on request method::

 [composite:main]
 use = egg:fluncrunner#request_method
 post = flunc

No automated implementation of the test inspection API is provided.
If you have a directory of static HTML forms that implement the API
for your flunc tests, you may want to configure a static file server
to respond to GET requests::

 [composite:main]
 use = egg:fluncrunner#request_method
 post = flunc
 get = static

 [app:static]
 use = egg:Paste#static
 document_root = %(here)s/ftest_forms/

The Paste static file server infers Content-type from file extensions,
so if you want to serve flunc test forms that don't have *.html names
you may want to use the provided `force_html` filter_factory which
sets Content-type: text/html on all responses::

 [app:static]
 use = egg:Paste#static
 document_root = %(here)s/ftest_forms/
 filter-with = force_html

 [filter:force_html]
 use = egg:fluncrunner#force_html

If you are not serving flunc-webrunner from Paste, you can configure
this WSGI pipeline in code. You can find the needed WSGI factories
in `fluncrunner`'s `main.py`, `force_html.py` and `request_method.py`.

Generating flunc test forms
===========================

This section wants writing.
