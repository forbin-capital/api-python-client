"""
This script permits to setup the python package.
"""

from setuptools import find_packages, setup


setup(

    # name on pypi
    name='forbin',

    # code version
    version=0.1,

    # List packages
    packages=find_packages(),

    author="Forbin Capital",
    author_email="contact@forbin-capital.com",

    description="Python client for Forbin API",

    long_description=open('README.md').read(),

    long_description_content_type="text/markdown",

    install_requires=["pandas",
                      "pytz",
                      "requests"],

    # Taking into account MANIFEST.in
    include_package_data=True,

    # Official page
    url='https://github.com/forbin-capital/api-python-client',

    # Some meta data:
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers.
    classifiers=['Intended Audience :: Science/Research',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Topic :: Software Development',
                 'Topic :: Scientific/Engineering',
                 'Operating System :: Microsoft :: Windows',
                 'Operating System :: POSIX',
                 'Operating System :: Unix',
                 'Operating System :: MacOS',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 ('Programming Language :: Python :: '
                  'Implementation :: CPython'),
                 ('Programming Language :: Python :: '
                  'Implementation :: PyPy')
                 ],

    # It's a plugin system, but we use it almost exclusively
    # To create commands, like "django-admin".
    # For example, if you want to create the fabulous "proclaim-sm" command, you
    # will point this name to the proclaim() function. The order will be
    # created automatically.
    # The syntax is "nom-de-commande-a-creer = package.module:fonction".
    entry_points={
        'console_scripts': [
        ],
    },

)