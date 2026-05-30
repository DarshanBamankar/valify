Installation
============

Requirements
------------

Python 3.10 or higher.

Install via pip
---------------

.. code-block:: bash

   pip install valify

Verify installation
-------------------

.. code-block:: python

   import valify
   print(valify.__version__)

Development installation
------------------------

To install valify for local development:

.. code-block:: bash

   git clone https://github.com/DarshanBamankar/valify
   cd valify
   python -m venv .venv
   .venv\Scripts\activate
   pip install -e ".[dev]"