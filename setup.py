from setuptools import setup

setup(name='ghgi',
      version='0.0.1',
      description='Greenhouse Gas Index',
      url='https://github.com/ghgindex/ghgi',
      author='GHGI',
      author_email='geoff@ghgi.org',
      license='CCv4-BY-SA',
      packages=['ghgi'],
      test_suite='nose.collector',
      tests_require=['nose', 'inflect'],
      zip_safe=False)
