import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid==1.4',
    'SQLAlchemy==0.8.0b2',
    'transaction==1.4.1',
    'pyramid_tm==0.7',
    'zope.sqlalchemy==0.7.2',
    'waitress==0.8.2',
    ]

setup(name='skaner',
      version='0.0',
      description='skaner',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='skaner',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = skaner:main
      [console_scripts]
      initialize_skaner_db = skaner.scripts.initializedb:main
      """,
      )
