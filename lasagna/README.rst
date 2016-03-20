Lasagna
=======

The application for Gordon.
It is a simple `flask app <http://flask.pocoo.org/>`__ which
serve the API and website.

Testing
-------

Here are some snippets to help develop and test:

* ``flake8 lasagna tests``, run the linter against source files

* ``py.test -v --tb=line --cov=lasagna --cov-report=html``,
  run tests and coverage

Optimizing
~~~~~~~~~~

Sometimes it could be interesting to profile code to identify bottlenecks,
here is a quick snippet to perform that:

Simply run tests with the following options

.. code-block:: bash

  python3 -m cProfile -o /tmp/profile $(which py.test)

Then create a python file to print those results

.. code-block:: python

  import pstats
  p = pstats.Stats('/tmp/profile')
  p.strip_dirs()
  p.sort_stats('cumtime')
  p.print_stats(50)
