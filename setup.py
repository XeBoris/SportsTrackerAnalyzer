#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Boris Bauermeister",
    author_email='Boris.Bauermeister@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="All you need to create a multi-user sports tracker database from multiple sources.",
    entry_points={
        'console_scripts': [
            'sportstrackeranalyzer=sportstrackeranalyzer.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    package_data={'sportstrackeranalyzer': ['configuration/*.config']},
    include_package_data=True,
    keywords='sportstrackeranalyzer',
    name='sportstrackeranalyzer',
    packages=find_packages(include=['sportstrackeranalyzer',
                                    'sportstrackeranalyzer.module',
                                    'sportstrackeranalyzer.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/XeBoris/sportstrackeranalyzer',
    version='0.1.0',
    zip_safe=False,
)
