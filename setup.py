#!/usr/bin/env python
# Learn more: https://github.com/un33k/setup.py
import os
import sys

from codecs import open
from shutil import rmtree
from setuptools import setup


package = 'slugify'
python_requires = ">=3.7"
here = os.path.abspath(os.path.dirname(__file__))

install_requires = ['text-unidecode>=1.3']
extras_requires = {'unidecode': ['Unidecode>=1.1.1']}
test_requires = []

about = {}
with open(os.path.join(here, package, '__version__.py'), 'r', 'utf-8') as f:
    exec(f.read(), about)

with open('README.md', 'r', 'utf-8') as f:
    readme = f.read()


def status(s):
    print('\033[1m{0}\033[0m'.format(s))


# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    try:
        status('Removing previous builds…')
        rmtree(os.path.join(here, 'dist'))
    except OSError:
        pass

    status('Building Source and Wheel (universal) distribution…')
    os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

    status('Uploading the package to PyPI via Twine…')
    os.system('twine upload dist/*')

    status('Pushing git tags…')
    os.system('git tag v{0}'.format(about['__version__']))
    os.system('git push --tags')
    sys.exit()

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    license=about['__license__'],
    packages=[package],
    package_data={'': ['LICENSE']},
    package_dir={'slugify': 'slugify'},
    include_package_data=True,
    python_requires=python_requires,
    install_requires=install_requires,
    tests_require=test_requires,
    extras_require=extras_requires,
    zip_safe=False,
    cmdclass={},
    project_urls={},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    entry_points={'console_scripts': ['slugify=slugify.__main__:main']},
)
