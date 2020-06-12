Test the Code Linter Extension
==============================

Just a normal paragraph.

.. code-block:: json

   { "json" : "data" }

.. code-block::

   $ don't lint this

.. code-block:: json

   $ invalid json

.. code-block:: yaml

   ---
   valid_yaml:
     - one
     - two
     - three

.. code-block:: yaml

   ---
   invalid-yaml:
   - one
   invalid


.. literalinclude:: test.json
   :language: json

.. don't lint code below, no language defined.
.. literalinclude:: test.json
