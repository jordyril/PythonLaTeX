"""
This module is the base module for saving .tex files using pylatex
..  :copyright: (c) 2019 by Jordy Rillaerts.
    :license: MIT, see License for more details.
"""

import os
import posixpath


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
            self._create_inputs_folder()
        # print("latexsaving init out")

    @property
    def _folder(self):
        return f"{self._folder_path}{self._folder_name}"

    def _absolute_path(self, name):
        path = posixpath.join(self._folder, name)
        return path

    def _relative_path(self, name):
        path = posixpath.join(self._folder_name, name)
        return path

    def _create_folder(self):
        if not os.path.exists(self._folder):
            os.makedirs(self._folder)

    def _create_inputs_folder(self):
        if not os.path.exists(f"{self._folder_path}Inputs"):
            os.makedirs(f"{self._folder_path}Inputs")

    @property
    def _inputs_folder(self):
        return f"{self._folder_path}Inputs/"

    def _write_input_to_txt_file(self, latex_input):
        with open(f"{self._inputs_folder}inputs.txt", "a") as file:
            file.write(latex_input)

    def _create_input_txt_file(self):
        with open(f"{self._inputs_folder}inputs.txt", "w") as file:
            text = "Summary of all Inputs".upper()
            n = len(text)
            file.write(f"{n * '='} \n")
            file.write(f"{text} \n")
            file.write(f"{n * '='} \n")

    def _print_latex_input(self, filename):
        to_print = (
            f"\n %Latex input: {filename} %\n" f"\\input{{Inputs/input_{filename}}} \n"
        )
        print(to_print)
        return to_print
