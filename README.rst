Gordon
======

A simple website to assist you on your everyday cooking

.. image:: https://travis-ci.org/IxDay/gordon.svg?branch=master
    :target: https://travis-ci.org/IxDay/gordon

Table of content
----------------

* `Requirements <#requirements>`__
* `Getting started <#getting-started>`__
* `Architecture <#architecture>`__
* `Contributing <#contributing>`__

Requirements
------------

In order to start the Gordon application and start coding you need to
install:

* `Docker <https://www.docker.com/>`__
* `Docker Compose <https://docs.docker.com/compose/>`__ 1.6+

That's it, all the development environment relies on docker, and compose
to orchestrate.

Getting started
---------------

Now we can bring the development environment up.

* Clone the repo ``git clone https://github.com/IxDay/gordon``

* Build it by running ``DB_PASSWORD=<password> docker-compose build``
  with password the value of the password you want for you development
  database.

* Then, fulfill the database by bringing the database helper container up:
  ``docker-compose run potatowatcher bash`` and now run the helper script:
  ``./helper.sh full_reinitialize``, you will see a lot of sql statements.
  Verify that everything is fine by connecting to the dabase for example
  (by typing ``./helper.sh``) and exit the container with the ``exit`` command.

* Install frontend dependencies by connecting to the container:
  ``docker-compose run --entrypoint /bin/bash front`` and typing ``npm install``

* Generate the assets by typing: ``docker-compose run front build``

* Once this is done we can connect to the container containing the API:
  ``docker attach gordon_api_1`` and install the development dependencies:
  ``pip install -e .[tests,dev]``

* The application is now ready to be started, just run the
  development server by typing: ``lasagna``, and now the application
  should be available at ``localhost:5000``

Architecture
------------

Gordon is a simple three tier architecture application. The code
is divided in folders which represent a part of it.

* `Potato <./potato>`__ is the database of the application, the
  directory contains some scripts to init the database, and helpers
  to connect.

* `Lasagna <./lasagna>`__ is the API and contains the business logic.

* `Dessert <./dessert>`__ is the frontend and provides css and javascript.

The Gordon environment is build upon Docker and Docker Compose,
all the part of the development and the application are contained
into *"containers"*. Here is a description of those:

**Note:** there is more containers than services, this is due to the need
of helpers tools which are also containerized

* **potato** this container runs the PostgreSQL database, it is automatically
  started and should not be modified or directly accessed.

* **potatowatcher** this is the database helper, it provides some scripts
  to access or initialized it, notably the
  `helper.sh file <./potato/helper.sh>`__

* **lasagna** the main container you will attach, contains the core application:
  `lasagna` and tools for development.

* **dessert** a simple container which generates the assets (css, javascript),
  it provides an entrypoint for `gulp <http://gulpjs.com/>`__ which is the
  tool to build.

Those containers description is stored into
`dockerfiles directory <./dockerfiles>`__ and the
`docker compose file <./docker-compose.yml>`__ describe how to start and
orchestrate them.

Contributing
------------

In order to contribute there is only one rule to respect: **MAKE TESTS PASS!**

Gordon aim to be heavily tested and documented, just be sure that all those
requirements are fulfilled and everything should go fine.

In order to run those tests you only have to run the following commands, into
the api container:

* ``flake8 lasagna tests``, this will run a linter accross the source files
  and display some style errors in code.

* ``py.test -v --tb=line --cov=lasagna --cov-report=html``, this will run
  tests against the code base and also generate a coverage report.
