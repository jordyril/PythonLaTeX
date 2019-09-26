"""
Created on Thur Sep 26 2019

@author: jordyril
"""

"""
   To create a source distribution of the pythonlatex
   package run

   python pythonlatex.py sdist

   which will create an archive file in the 'dist' subdirectory.
   The archive file will be  called 'pythonlatex-1.0.zip' and will
   unpack into a directory 'pythonlatex-1.0'.

   An end-user wishing to install the pythonlatex package can simply
   unpack 'pythonlatex-1.0.zip' and from the 'pythonlatex-1.0' directory and
   run

   python setup.py install

   which will ultimately copy the pythonlatex package to the appropriate
   directory for 3rd party modules in their Python installation
   (somewhere like 'c:\python27\libs\site-packages').

   To create an executable installer use the bdist_wininst command

   python setup.py bdist_wininst

   which will create an executable installer, 'pythonlatex-1.0.win32.exe',
   in the current directory.

"""

from setuptools import setup

# ====================================================================
# OPTIONS
# ====================================================================
# package naming
DISTNAME = "pythonlatex"

# descriptions
DESCRIPTION = "'pythonlatex' package version"
LONG_DESCRIPTION = "'pythonlatex' package and extensions\n"

# developer(s)
AUTHOR = "Jordy Rillaerts"
EMAIL = "jordy_rillaerts13@hotmail.com"

# versioning
MAJOR = 0
MINOR = 0
MICRO = 1
ISRELEASED = False
VERSION = "%d.%d.%d" % (MAJOR, MINOR, MICRO)
QUALIFIER = ""

FULLVERSION = VERSION
write_version = True

if not ISRELEASED:
    FULLVERSION += ".dev"

CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Operating System :: OS Independent",
    "Intended Audience :: Jordy Rillaerts",
    "Programming Language :: Python :: 3.7",
    "Topic :: Support",
]

# ====================================================================
# Create setup
# ====================================================================
setup(
    name=DISTNAME,
    version=FULLVERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    maintainer=AUTHOR,
    maintainer_email=EMAIL,
    long_description=LONG_DESCRIPTION,
    setup_requires=["pylatex"],
    install_requires=["pylatex"],
    packages=["pythonlatex"],
)
