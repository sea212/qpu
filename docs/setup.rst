Setup
=====
Requires: Python >= 3.4

| Install package: ``pip install qpu``
| Install test tools: ``pip install qpu[TEST]``
| Install linter (for tox tests): ``pip install qpu[LINT]``
| Install documentation tools: ``pip install qpu[DOCS]``
| Install everything: ``pip install qpu[ALL]``

Test
----
| Without tox (no linter checks): ``python setup.py test``
| With tox: ``python -m tox``

Generate documentation
----------------------
``python setup.py docs``
