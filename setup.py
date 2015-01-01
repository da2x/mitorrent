# -*- coding: utf-8 -*-

from multiprocessing import freeze_support
from setuptools import setup
import sys


if sys.version < '3.2':
    print('Requires Python 3.2 or newer.', file=sys.stderr)
    sys.exit(1)

setup(author='Daniel Aleksandersen',
      author_email='private',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3 :: Only',
          'Topic :: Communications :: File Sharing',
          'Topic :: Internet',
          'Topic :: Utilities'],
      description='BitTorrent metainfo file (.torrent) creation utility',
      entry_points={
          'console_scripts': [
              'mitorrent = mitorrent.mitorrent:main'
          ]
      },
      install_requires=[
          'setuptools'
      ],
      keywords=['BitTorrent', 'torrent'],
      license='BSD 2-Clause License',
      long_description=open('README', 'r').read(),
      name='mitorrent',
      packages=[
          'mitorrent'
      ],
      test_suite='tests',
      url='https://www.aeyoun.com/projects/mitorrent/index.html',
      version='0.9.6')

if __name__ == '__main__':
    freeze_support()
