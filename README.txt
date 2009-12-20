flunc-webrunner runs flunc tests (suites of twill scripts with variables) through the web.

The API
=======

There is a web API for running a flunc test.

Executing a test
----------------

To execute a test, POST to the test's URI /name/of/flunc/test/

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

To discover the available variables for a test, GET the test's URI.

An HTML form will be returned, suitable for POSTing back to the server.

If available, default values (from the test's corresponding .conf) will be
detailed in the form fields' pre-filled values.

Configuring the server
======================

This section wants writing.
