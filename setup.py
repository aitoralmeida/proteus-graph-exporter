# -*- coding: utf-8 -*-

#-*-*- encoding: utf-8 -*-*-
from setuptools import setup

# TODO: select categories
classifiers=[
    "Development Status :: 3 - Alpha",
    "Environment :: Web Environment",
    "Intended Audience :: Developers",
    "License :: Freely Distributable",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Topic :: Internet :: WWW/HTTP",
    "Topic :: Software Development :: Libraries :: Application Frameworks",
]

cp_license="MIT"

setup(name='graph-exporter',
      version='0.1',
      description="A  library to export graphs to different formats",
      classifiers=classifiers,
      author='Aitor Almeida',
      author_email='aitor.almeida@deusto.es',
      url='http://github.com/aitoralmeida/graph-exporter',
      license=cp_license,
      py_modules=['graph_exporter'],
     )