# -*- coding: utf-8 -*-
"""
This module contains the tool of slc.tasks
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.1'

long_description = (
    read('README.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('README.txt')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    'Download\n'
    '********\n')

tests_require = ['zope.testing']

setup(name='slc.tasks',
      version=version,
      description="To facilitate organisation and management of tasks.",
      long_description=long_description,
      classifiers=[
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        "License :: OSI Approved :: European Union Public Licence 1.1 (EUPL 1.1)",
        ],
      keywords='osha plone task project management',
      author='Syslab.com GmbH',
      author_email='info@syslab.com',
      url='https://svn.syslab.com/svn/OSHA/slc.tasks',
      license='GPL + EUPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['slc'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite='slc.tasks.tests.test_docs.test_suite',
      entry_points="""
      # -*- entry_points -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
