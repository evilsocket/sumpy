from setuptools import setup, find_packages

import sumpy
import os


desc = 'Python client for Sum linear algebra database.'

setup( name                 = 'sum-py',
       version              = sumpy.__version__,
       description          = desc,
       long_description     = desc,
       long_description_content_type = 'text/plain',
       author               = sumpy.__author__,
       author_email         = sumpy.__email__,
       url                  = 'http://www.github.com/evilsocket/sumpy',
       packages             = find_packages(),
       python_requires      = ">=3.0",

       license              = sumpy.__license__,
       classifiers          = [
           'Development Status :: 5 - Production/Stable',
           'Environment :: Console',
           'Intended Audience :: Developers',
           'License :: OSI Approved :: GNU General Public License (GPL)',
           'Operating System :: OS Independent',
           'Programming Language :: Python',
           'Programming Language :: Python :: 3']
)
