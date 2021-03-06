# -*- coding: utf-8
from distutils.core import setup
setup(
  name = 'Flask-KQMaps',
  packages = ['flask_kqmaps'], 
  package_data={'flask_kqmaps': ['templates/*', 'static/*', 'static/*/*', 'static/*/*/*', 'static/*/*/*/*', 'static/*/*/*/*/*', 'static/*/*/*/*/*/*', 'static/*/*/*/*/*/*/*'], },
  version = '0.4.2',
  license='GNU GPLv3',
  description = 'Flask Extension for KQWebMap API for Leaflet (aka KQClient for Leaflet API)',
  author = 'Yi QI',
  author_email = 'jnjnqy@gmail.com',
  url = 'https://github.com/sunshinejnjn/flask_kqmaps',
  download_url = 'https://github.com/sunshinejnjn/flask_kqmaps/archive/refs/tags/v0.4.tar.gz',
  keywords = ['KQGIS', 'cangqiong', '苍穹', 'GIS', 'KQ', 'leaflet', 'webgis', 'kqmaps', 'flask_kqmaps', 'flask-kqmaps', 'flask'],
  install_requires=[
          'flask',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3',
    'Framework :: Flask',
  ],
)