Dessert
=======

A simple and sweet design system

Tasks
-----
Usage: `gulp` (calls default task) or `gulp [task_name]`

Available tasks are:

* ``clean``:         deletes the ``dist`` folder
* ``fonts``:         copies all the fonts from ``fonts`` folder to the ``dist``
  folder
* ``styles``:        compiles all the SASS files into a single and linted
  CSS ``main.css``
* ``build``:         **builds a developper friendly version dessert
  (default task)**
* ``watch:styles``:  runs the ``styles`` task when a SASS file is modified

Project organisation
--------------------

.. code-block:: text

  /src
  ├── fonts
  ├── scripts
  └── styles


Documentation
-------------
The documentation of the project is available in the `docs <./docs>`__ folder.

Browser support
-------
Dessert is designed to support the latest two versions (current and previous) of modern web browsers.

TODO
----

* ~~Grid system~~
* ~~Buttons~~
* Forms
* Menu
* Navigation
* Modals
