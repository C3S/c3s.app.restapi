c3s.app.restapi -- a RESTful API for the Cultural Commons Collecting Society (C3S)
===================================================================================

.. image:: https://ci2.c3s.cc/job/c3s.api/badge/icon
   :target: https://ci2.c3s.cc/job/c3s.api/


This project is a starting point for an API.

As of now, this is just a working set of REST API stubs, so the examples for
GET, POST, PUT and DELETE requests are working and tested,
but not very meaningful. More to come.


Cornice
--------

This project uses Cornice to build REST services.

Source: https://github.com/mozilla-services/cornice

Documentation: http://cornice.readthedocs.org/


Services
---------

The REST services are defined in src/c3s/api/views.py, including samples
for GET, PUT, POST and DELETE. Tests are in src/c3s/api/tests/test_views.py.


Documentation
--------------

Cornice offers a Sphinx extension to automagically create documentation
from the docstrings etc. contained in the code.

The docs (using Sphinx) are in the subfolder `docs/source`
and you can build them locally by calling `bin/sphinx`
after having run buildout (see ci.sh).
