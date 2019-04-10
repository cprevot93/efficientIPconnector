# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='efficientIPconnector',
    version='0.1',
    description='Manage fortiManager objects with efficientIP IPAM solution',
    long_description=readme,
    author='Charles Prevot',
    author_email='cprevot@fortinet.com',
    url='https://github.com/SelR4c/efficientIPconnector',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

