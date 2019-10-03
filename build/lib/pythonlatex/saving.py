"""
This module is the base module for saving .tex files using pylatex
..  :copyright: (c) 2019 by Jordy Rillaerts.
    :license: MIT, see License for more details.
"""

import os
import posixpath


class LatexSaving(object):
    """
    Class for my standardised formats, saving of the plain object
    should be done in the 'inner' folder, while the .tex file that can
    be imported in latex should be saved in the 'outer' folder
    e.g. a pure plot is saved in the 'inner' folder, while the full
    figure (with caption, label,... within figure environment) is saved
    in the 'outer' folder
    e.g. same reasoning for table: tabular gets saved in the 'inner',
    while full table is saved in 'outer'
    """

    def __init__(
        self, folders_path="Latex/", outer_folder="Outer", inner_folder="Inner"
    ):
        # print("latexsaving init in")
        self._folders_path = folders_path
        self._inner_folder_name = inner_folder
        self._outer_folder_name = outer_folder
        self._create_folders()
        self._create_latest_inputs_txt()

    def _create_folders(self):
        for folder_name in [self._inner_folder_name, self._outer_folder_name]:
            if not os.path.exists(self._folder(folder_name)):
                os.makedirs(self._folder(folder_name))

    def _folder(self, folder_name):
        return f"{self._folders_path}{folder_name}"

    @property
    def _inner_folder(self):
        return self._folder(self._inner_folder_name)

    @property
    def _outer_folder(self):
        return self._folder(self._outer_folder_name)

    def _absolute_inner_path(self, name):
        path = posixpath.join(self._inner_folder, name)
        return path

    def _relative_inner_path(self, name):
        path = posixpath.join(self._inner_folder_name, name)
        return path

    def _absolute_outer_path(self, name):
        path = posixpath.join(self._outer_folder, name)
        return path

    def _relative_outer_path(self, name):
        """
        Not really used, just for completeness
        """
        path = posixpath.join(self._outer_folder_name, name)
        return path

    @property
    def _latest_inputs_file(self):
        return f"{self._absolute_outer_path('latest_inputs')}.txt"

    def _create_latest_inputs_txt(self):
        with open(self._latest_inputs_file, "w") as file:
            text = f"Summary of all {self._inner_folder_name}".upper()
            n = len(text)
            file.write(f"{n * '='} \n")
            file.write(f"{text} \n")
            file.write(f"{n * '='} \n")

    def _write_input_to_txt_file(self, latex_input):
        with open(self._latest_inputs_file, "a") as file:
            file.write(latex_input)

    def _print_latex_input(self, filename):
        to_print = (
            f"\n %Latex input: {filename} %\n"
            f"\\input{{{self._relative_outer_path(filename)}}} \n"
        )
        print(to_print)
        return to_print

    ########

    # def _absolute_path(self, name):
    #     path = posixpath.join(self._folder, name)
    #     return path

    # def _relative_path(self, name):
    #     path = posixpath.join(self._folder_name, name)
    #     return path

    # def _create_folder(self):
    #     if not os.path.exists(self._folder):
    #         os.makedirs(self._folder)

    # def _create_inputs_folder(self):
    #     if not os.path.exists(f"{self._folders_path}Inputs"):
    #         os.makedirs(f"{self._folders_path}Inputs")

    # @property
    # def _inputs_folder(self):
    #     return f"{self._folders_path}Inputs/"

    # def _write_input_to_txt_file(self, latex_input):
    #     with open(f"{self._inputs_folder}inputs.txt", "a") as file:
    #         file.write(latex_input)

    # def _create_input_txt_file(self):
    #     with open(f"{self._inputs_folder}inputs.txt", "w") as file:
    #         text = "Summary of all Inputs".upper()
    #         n = len(text)
    #         file.write(f"{n * '='} \n")
    #         file.write(f"{text} \n")
    #         file.write(f"{n * '='} \n")

    # def _print_latex_input(self, filename):
    #     to_print = (
    #         f"\n %Latex input: {filename} %\n" f"\\input{{Inputs/input_{filename}}} \n"
    #     )
    #     print(to_print)
    #     return to_print
