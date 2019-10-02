"""
This module modifies the 'Table' class from 'pylatex'
..  :copyright: (c) 2019 by Jordy Rillaerts.
    :license: MIT, see License for more details.
"""

from pylatex import Table as TableOriginal
from pylatex import Package, NoEscape
from .saving import LatexSaving


class Table(LatexSaving, TableOriginal):
    """A class that represents a Table environment with modified methods compared to parent"""

    def __init__(
        self,
        *args,
        folder_path="Latex/",
        folder_name="Tables",
        create_folder=True,
        position=None,
        **kwargs,
    ):
        # print("saving init in")
        LatexSaving.__init__(
            self,
            folder_name=folder_name,
            folder_path=folder_path,
            create_folder=create_folder,
        )
        # print("saving init out")
        # print("figure init in")
        TableOriginal.__init__(self, *args, position=position, **kwargs)
        # print("figure init out")

    # def input_from_to_latex_string(
    #     self,
    #     to_latex_string,
    #     name,
    #     caption,
    #     label=None,
    #     above=True,
    #     **latex_input_kwargs,
    # ):
    #     # write to_latex_tabular to .tex file - create tabular file
    #     with open(self._absolute_path + name + self._extension, "w") as file:
    #         file.write(to_latex_string)
    #     self.create_latex_input(name, caption, label, above, **latex_input_kwargs)

    #     return None
