import os.path

_EXCLUDED = ['__init__.py']

TEMPLATE_FILES = [
    (file, os.path.join(os.path.dirname(__file__), file))
    for file in os.listdir(os.path.dirname(__file__))
    if os.path.isfile(os.path.join(os.path.dirname(__file__), file)) and file not in _EXCLUDED
]
