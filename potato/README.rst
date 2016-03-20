Potato
======

The application database, this database will be available internally,
external functions will be provided by the API.

Technologies
------------

* PostgreSQL: an object-relational database management system,
[official website](http://www.postgresql.org/).

Connect to database
-------------------

It is possible to interact directly with the database through a shell,
by running the following commands:

* ``docker-compose run potatowatcher bash``: start and attach the watcher.
* ``make connect``: connect to the database.


Consult volumes (logs, config)
------------------------------

To consult volumes we only have to connect the potato volumes to a simple
container: `docker run --rm --volumes-from potato -ti busybox sh`

The files will be available in the place where volumes were mounted in
`dockerfile <../dockerfiles/dockerfile-potato)>`__, e.g:

* ``/etc/postgresql``
* ``/var/log/postgresql``
* ``/var/lib/postgresql``

