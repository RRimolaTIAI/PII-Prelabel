# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scripts']

package_data = \
{'': ['*']}

install_requires = \
['gooey>=1.0,<2.0', 'pandas>=1.5,<2.0', 'psutil>=5.9,<6.0', 'spacy>=3.4,<4.0']

setup_kwargs = {
    'name': 'prelabel-ne',
    'version': '0.2.1',
    'description': 'NER pre-labeling for Oracle projects.',
    'long_description': None,
    'author': 'Jari Peräkylä',
    'author_email': 'jari.perakyla@telusinternational.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
