*********************
eduGAIN XML validator
*********************

This is a small script that can be used to validate eduGAIN XML data. The script
works with annexed XSD resources located in `schemas/` directory, that are use used
to validate the eduGAIN XML data.


Usage
=====

After copied the script and the schemas (you can simply clone the repo as usual).
To make the script works you have to install the *xmlschema* library in a Python
2.7 or Python 3.5+ \environment. This can be done with the *pip* package manager
using the command::

    pip install xmlschema~=1.0.16

or alternatively using the requirements file::

    pip install -r requirements.txt

To check the XML data execute the script passing path to eduGAIN data file, eg.::

    edugain_validate.py edugain-v1.xml


License
=======

This software is distributed under the terms of the BSD 3-Clause License.
See the file 'LICENSE' in the root directory of the present
distribution, or https://opensource.org/licenses/BSD-3-Clause.

