*********************
eduGAIN XML validator
*********************

This is a small script that can be used to validate
`eduGAIN XML metadata <https://technical.edugain.org/metadata>`_.
The script works with annexed XSD resources located in `schemas/` directory,
that are use used to validate the eduGAIN XML data.


Dependencies installation
=========================

After copied the script and the schemas (you can simply clone the repo as usual).
To make the script works you have to install the libraries
`signxml <https://github.com/XML-Security/signxml>`_ and
`xmlschema <https://github.com/brunato/xmlschema>`_ in
a Python Python 3.5+ environment. This can be done with the *pip* package manager
using the command::

    pip install signxml xmlschema

or alternatively using the requirements file::

    pip install -r requirements.txt

.. note::
    These commands work if you use a Python's virtual environment or if you have
    administrative privileges. Otherwise you can do a user-space installation
    with `--user` option.


Usage
=====

To check the XML data execute the script providing as argument the path to eduGAIN data file, eg.::

    python edugain_validate.py edugain-v1.xml

If you also want to validate XML signature use the option `--cert`, providing the path
to the file containing the signing key::

    ./edugain_validate.py --cert=mds-v1.cer edugain-v1.xml

For other script's options use ``./edugain_validate.py --help``.


License
=======

This software is distributed under the terms of the BSD 3-Clause License.
See the file 'LICENSE' in the root directory of the present
distribution, or https://opensource.org/licenses/BSD-3-Clause.

