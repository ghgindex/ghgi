from setuptools import setup
from pathlib import Path

datadir = Path(__file__).parent / 'ghgi' / 'datasets'
pkgdir = Path(__file__).parent / 'ghgi'
files = [str(p.relative_to(pkgdir)) for p in datadir.rglob('*.json')]
files += [str(p.relative_to(pkgdir)) for p in datadir.rglob('*.py')]

setup(
      name='ghgi',
      version='0.0.1',
      description='Greenhouse Gas Index',
      url='https://github.com/ghgindex/ghgi',
      author='GHGI',
      author_email='geoff@ghgi.org',
      license='CCv4-BY-SA',
      packages=['ghgi'],
      package_data={
            'ghgi': files
      },
      test_suite='nose.collector',
      tests_require=['nose', 'inflect'],
      install_requires=['inflect'],
      zip_safe=False
)
