from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='fluncrunner',
      version=version,
      description="Run flunc tests through the web",
      long_description=open("README.txt").read(),
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='',
      author_email='',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'flunc',
        'PasteDeploy',
        'WebOb',
        'pastables',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [paste.app_factory]
      main = fluncrunner.main:app_factory

      [paste.composite_factory]
      request_method = fluncrunner.request_method:composite_factory

      [paste.filter_factory]
      force_html = fluncrunner.force_html:filter_factory
      """,
      )
