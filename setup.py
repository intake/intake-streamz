#!/usr/bin/env python

from setuptools import setup, find_packages
import versioneer


requires = open('requirements.txt').read().strip().split('\n')

setup(
    name='intake-streamz',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='streamz plugin for Intake',
    url='https://github.com/intake/intake-streamz',
    maintainer='Martin Durant',
    maintainer_email='mdurant@anaconda.com',
    license='BSD',
    py_modules=['intake_streamz'],
    packages=find_packages(),
    entry_points={
        'intake.drivers': ['streamz = intake_streamz.source:StreamzSource']},
    include_package_data=True,
    install_requires=requires,
    long_description=open('README.md').read(),
    zip_safe=False,
)
