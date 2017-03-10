from setuptools import setup

setup(
    name='dicttools',
    version='1.1.6',
    packages=['dicttools', 'dicttools.tests'],
    test_suite='dicttools.tests',
    url='https://github.com/trzemecki/dicttools',
    license='Apache 2.0',
    author='Leszek Trzemecki',
    author_email='leszek.trzemecki@gmail.com',
    description='Additional dictionary functions for python.',
    install_requires=[
        'mock', 'six'
    ],
)
