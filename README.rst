=====================
SportsTrackerAnalyzer
=====================


.. image:: https://img.shields.io/pypi/v/sportstrackeranalyzer.svg
        :target: https://pypi.python.org/pypi/sportstrackeranalyzer

.. image:: https://img.shields.io/travis/XeBoris/sportstrackeranalyzer.svg
        :target: https://travis-ci.com/XeBoris/sportstrackeranalyzer

.. image:: https://readthedocs.org/projects/sportstrackeranalyzer/badge/?version=latest
        :target: https://sportstrackeranalyzer.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


ReadMe
------

All you need to create a multi-user sports tracker database from multiple sources.

* Free software: MIT license
* Documentation: https://sportstrackeranalyzer.readthedocs.io.

This is the worst README ever, but the sportstrackeranalyzer is already in first state where some functionality is given.
In case you have asked for a collection of all your data from Runtastic, you can already read-in the database dump, according
to a simple file-based structure on disk (after you have unpacked the database dump). Follow the following steps:

1) Download and Installation:

git clone REPO

make install

2) Add a new database location, database type and name:

sportstrackeranalyzer createDB testDB --type FileDataBase --path /home/user/test-database-dir

3) Tell your system which sportstrackeranalyzer database you would like to use

sportstrackeranalyzer loadDB testDB --type FileDataBase --path /home/user/test-database-dir

4) An empty database needs a user first! Add one...

sportstrackeranalyzer addUser

5) You need to tell your database which user you would like to use by default for further operations:

sportstrackeranalyzer setUser <username>

6) Import your Runtastic tracks from the database dump:

sportstrackeranalyzer addTracks --source-type database --track-source runtastic --path /path/to/RunTastic_Exports/


--> No further tests made at this point! Development is ongoing! Don't be mad if not working as expected.


Features
--------

* Still a lot...

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
