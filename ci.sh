#!/bin/bash
#
# This script is used for continuous integration.
# You can see how the package is set up.
#
echo "starting setup and continuous integration"

# create a virtualenv 
virtualenv env

# use that virtualenv
#. env/bin/activate
# ^that's how you would use it on a shell,
# but for jenkins I prefer explicit paths, see below

# bootstrap the buildout
env/bin/python bootstrap.py
# this will create a script bin/buildout

# run the buildout
bin/buildout
# this sets up things according to the buildout.cfg
# e.g. a script bin/sphinx to generate the documentation

# create the documentation
bin/sphinx

# set up the package for development and testing
env/bin/python setup.py develop

# run the tests
#env/bin/test
env/bin/pip install nose coverage
env/bin/nosetests --with-coverage --cover-html --with-xunit
