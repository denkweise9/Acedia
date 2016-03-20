import os

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt'), encoding='utf-8') as f:
    CHANGES = f.read()


setup(
    name='sloth',
    version='0.1',
    description='',
    long_description=README,
    license='AGPLv3',
    # TODO: add author info
    #author='',
    #author_email='',
    url='https://github.com/Lvl4Sword/Sloth/',
    # TODO: add keywords
    #keywords='',
    install_requires = ['python-dateutil'],
    classifiers = [
        "License :: OSI Approved :: GNU Affero General Public License v3"
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
    packages=find_packages(include=['sloth']),
    include_package_data=True,
    zip_safe=False,
    entry_points="""\
    [console_scripts]
    sloth-game = sloth.start:run
    """,
)
