# -*- coding: utf-8 -*-

#-*-*- encoding: utf-8 -*-*-
from setuptools import setup

# TODO: select categories
classifiers=[
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: Freely Distributable",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

cp_license="MIT"

setup(name='graph-exporter',
      version='0.2',
      description="A  library to export network graphs to different formats",
      classifiers=classifiers,
      author='Aitor Almeida',
      author_email='aitor.almeida@deusto.es',
      url='http://github.com/aitoralmeida/graph-exporter',
      license=cp_license,
      py_modules=['graph_exporter'],
     )
