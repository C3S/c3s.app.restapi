""" Setup file.
"""
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

requires = [
    'pyramid',
    'cornice',
    'PasteScript',
    'waitress'
    ]
test_requires = [
    'webtest',
    'nose',
    'coverage',
    ]

setup(name='c3s.api',
      version='0.1dev',
      description='an API for c3s',
      long_description=README,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application"
        ],
      keywords="web services",
      author='Christoph Scheid',
      author_email='c@c3s.cc',
      url='http://c3s.cc',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['c3s'],
      include_package_data=True,
      zip_safe=False,
      install_requires=requires + test_requires,
      entry_points="""\
      [paste.app_factory]
      main = c3s.api:main
      """,
      paster_plugins=['pyramid'],
      )
