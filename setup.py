from distutils.core import setup

setup(
    name='dicttools',
    version='1.0.0',
    packages=['tests', 'dicttools'],
    url='https://github.com/trzemecki/dicttools',
    license='Apache 2.0',
    author='Leszek Trzemecki',
    author_email='leszek.trzemecki@gmail.com',
    description='Additional dictionary functions for python.',
    requires=['mock']
)
