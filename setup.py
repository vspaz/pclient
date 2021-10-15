import os

import setuptools


def _build_path(file_path, base=os.path.abspath(os.path.dirname(__file__))):
    return os.path.join(base, file_path)


def _get_dependencies():
    with open(_build_path(file_path='requirements/prod.txt')) as fh:
        return [line.strip() for line in fh.readlines()]


def _get_readme():
    with open(_build_path(file_path='README.md')) as fh:
        return fh.read()


def _get_package_info():
    with open(_build_path(file_path='pyclient/__version__.py')) as fh:
        package_info = dict()
        exec(fh.read(), package_info)
        return package_info


_PACKAGE_INFO = _get_package_info()

setuptools.setup(
    name=_PACKAGE_INFO['title'],
    version=_PACKAGE_INFO['version'],
    description=_PACKAGE_INFO['description'],
    long_description=_get_readme(),
    packages=setuptools.find_packages(exclude=['tests', 'requirements']),
    install_requires=_get_dependencies(),
    url=_PACKAGE_INFO['url'],
    license='',
    author=_PACKAGE_INFO['author'],
    author_email=_PACKAGE_INFO['email'],
    maintainer=_PACKAGE_INFO['maintainer'],
    classifiers=[
        'Programming Language :: Python :: 3'
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
