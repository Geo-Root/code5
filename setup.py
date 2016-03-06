#!/usr/bin/env python
from __future__ import unicode_literals
import io
import os
from setuptools import setup, find_packages


setup(
    name='code5',
    version='5.1.post',
    url='https://github.com/Geo-Root/code5',
    description='UUID Code image generator',
    author='Faical Yannick Palingwende Congo',
    author_email='yannick.congo@gmail.com',
    platforms=['any'],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'c5 = code5.console_scripts:main',
        ],
    },
    install_requires=['six'],
    data_files=[('share/man/man1', ['docs/c5.1'])],
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
