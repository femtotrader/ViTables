.. |geq| unicode:: U+02265 .. greater than or equal symbol

Introduction
++++++++++++



Overview
********

`ViTables` is a member of the `PyTables` family. It's a graphical tool for browsing and editing files in both PyTables and `HDF5` formats. With `ViTables` you can easily navigate through data hierarchies, request metadata, view
real data and much more.

`ViTables` is being developed using `Python` and `PyQt`, the bindings of `Qt` libraries, so it can run on any platform that supports these components (which includes Windows, Mac OS X, Linux and many other Unices). The interface and features will remain the same on all platforms.

Efficiency and low memory requirements are guaranteed by the fact that data is loaded only when the object that contains it is opened and by the use of data buffers for dealing with large datasets.

Capabilities
************

The current release provides browsing, displaying, editing and querying capabilities. Some of them are listed below. Details are discussed in the related chapters.

Browsing and displaying capabilities
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Display data hierarchy as a fully browsable object tree.

- Open several files simultaneously.

- Open files in write mode as well as in read-only mode, disabling all editing functions.

- Display file information (path, size, number of nodes…).

- Display node (group or leaf) properties, including metadata and attributes.

- Display numerical arrays, i.e. homogeneous tables.

- Display heterogeneous table entities, i.e. records.

- Display multidimensional table cells.

- Unlimited zoom into the inner dimensions of multidimensional table cells.

Editing capabilities
^^^^^^^^^^^^^^^^^^^^

These editing features have been implemented for the object tree [#f1]_:

- File creation and renaming.

- Node creation (only for groups), renaming and deletion.

- Ability to copy and move nodes from their location to a different one, even in different files.

- Attribute creation, renaming and deletion.

All these changes automatically update the database (i.e. the file) to which the nodes belong.

Other
^^^^^

Other nice features include:

- *Ability to smoothly navigate really large datasets*.

- Support for doing complex table queries with a low memory footprint.

- Import from CSV files.

- Flexible plugins framework. A bunch of useful plugins are already included, see the :ref:`Appendix A<appendix-a>` for
  details.

- Configurable look and feel.

- A logger area, where errors and warnings (if any) are printed.

- Several levels of help are available: users guide, context help, tooltips and status bar.

We have paid special attention to usability issues so making use of these features is intuitive and pleasant.
Nevertheless, and just in case, we are providing this guide :-).

System Requirements
*******************

To run `ViTables` you need to install recent versions of `Python3`, `PyTables` (so you have to fulfil its own requirements) and `PyQt`. For instance, it runs smoothly with `Python` 3.11, `PyTables` 3.8 and `PyQt` 6.5.

At the moment, `ViTables` has been fully tested on Linux and Windows 10 platforms. Other Unices should run just fine when using the Linux version because all the software that `ViTables` relies on (i.e. `Python`, `Qt`, `PyQt`, `HDF5` and `PyTables`) is known to run fine on many Unix platforms as well.

Installation
************



Linux
^^^^^

A pyproject.toml (with `hatch` as a build-system) is used to build `ViTables`. You can install
the package from PyPI issuing the command::

  $ pip install ViTables

If you don't have any version of `PyQt` installed you can pass it as an extra to the above command::
  
   $ pip install ViTables[PyQt6]

In theory `PySide6` should work too but it has not been tested.

Windows and Mac OS X
^^^^^^^^^^^^^^^^^^^^

Currently there are no graphical installers available for these platforms. You
have to install `ViTables` from the command line, using the method described in the Linux section.


Further Reading
***************

General information about `PyTables` can be found at `its project site <https://www.pytables.org>`_.

Questions and feedback can be mailed to the developers.

.. rubric:: Footnotes

.. [#f1] Dataset editing capabilities have not yet been implemented.
