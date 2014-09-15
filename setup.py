try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Human Activity Recognition',
    'author': 'Saeed Partonia',
    'url': 'spartonia.github.io/ActRec',
    'download_url': 'https://github.com/spartonia/ActRec.git',
    'author_email': 'saeed.partonia@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['ActRec'],
    'scripts': [],
    'name': 'ActRec'
}

setup(**config)
