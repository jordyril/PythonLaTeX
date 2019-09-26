"""
This module is the base module for saving .tex files using pylatex
..  :copyright: (c) 2019 by Jordy Rillaerts.
    :license: MIT, see License for more details.
"""

import os


class LatexSaving(object):
    """
    Class for my standardised formats
    """

    def __init__(self, folder_path="Latex/", folder_name="Folder", create_folder=True):
        # print("latexsaving init in")
        self._folder_path = folder_path
        self._folder_name = folder_name
        if create_folder:
            self._create_folder()
        # print("latexsaving init out")

    @property
    def _folder(self):
        return f"{self._folder_path}{self._folder_name}"

    # @property
    # def _absolute_path(self):
    #     path = f"{self._folder()}/"
    #     return path

    # @property
    # def _relative_path(self):
    #     path = f"{self.__str__()}s/"
    #     return path

    def _create_folder(self):
        if not os.path.exists(self._folder):
            os.makedirs(self._folder)
