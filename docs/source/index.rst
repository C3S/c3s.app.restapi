=========
A Test
=========

.. note:: this is a test of cornice's autodocumentation feature.

          the following docs are auto-generated from the API Service's code,
	  see the **source** of this page and **src/c3s/api/views.py**.

moo

Hints
------

A few tips about working with cornice and sphinx:

 - Sphinx will find the cornice services in the source files
   and pick up the **docstrings**. Using ReST notation in there somehow works. :-)

 - You have to **change the .rst file referencing the cornice services** (e.g. this index.rst)
   to make sphinx reread the source files whose services are to be autodocumented.
   If you don't change the referencing file (even adding removing whitespace helps),
   then **changes will not be picked up**.

.. services::
   :modules: c3s.api.views


