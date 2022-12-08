"""
Created on Thur Sep 26 2019

@author: jordyril
"""

"""
   To create a source distribution of the pythonlatex
   package run

   python pythonlatex.py sdist

   which will create an archive file in the 'dist' subdirectory.
   The archive file will be  called 'pythonlatex-X.x.zip' and will
   unpack into a directory 'pythonlatex-X.x'.

   An end-user wishing to install the pythonlatex package can simply
   unpack 'pythonlatex-X.x.zip' and from the 'pythonlatex-X.x' directory and
   run

   python setup.py install

   which will ultimately copy the pythonlatex package to the appropriate
   directory for 3rd party modules in their Python installation
   (somewhere like 'c:\python27\libs\site-packages').

   To create an executable installer use the bdist_wininst command

   python setup.py bdist_wininst

   which will create an executable installer, 'pythonlatex-X.x.win32.exe',
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
with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

# developer(s)
AUTHOR = "Jordy Rillaerts"
EMAIL = "jordy_rillaerts13@hotmail.com"

URL = "https://github.com/jordyril/PythonLaTeX"

# versioning
MAJOR = 1
MINOR = 1
MICRO = 3
ISRELEASED = True
VERSION = "%d.%d.%d" % (MAJOR, MINOR, MICRO)
QUALIFIER = ""

FULLVERSION = VERSION
write_version = True

if not ISRELEASED:
    FULLVERSION += ".dev"

DEPENDENCIES = []
with open("requirements.txt", "r", encoding="utf-8") as requirements:
    for line in requirements:
        DEPENDENCIES.append(line.strip())

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
    url=URL,
    long_description_content_type="test/markdown",
    install_requires=DEPENDENCIES,
    packages=[DISTNAME],
)
