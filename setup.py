# -*- coding: utf-8 -*-
import sys
import os
from setuptools import setup, find_packages

sys.path.insert(0, os.path.abspath("src"))


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''

setup(
    name="couchdblogger",
    version='0.0.3',
    description=read('DESCRIPTION'),
    keywords="couchdb logging logger handler",
    author="Rinat F Sabitov",
    author_email="rinat.sabitov@gmail.ru",
    maintainer='Rinat F Sabitov',
    maintainer_email='rinat.sabitov@gmail.com',
    url="https://github.com/histrio/python-couchdblogger",
    package_dir={'': 'src'},
    packages=[".",],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Environment :: Web Environment',
        'Natural Language :: Russian',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=['requests'],
    include_package_data=True,
    zip_safe=False,
    long_description=read('README'),
    test_suite='test',
    tests_require=['mock==1.0.1',
		   'nose==1.3.1'],
)
