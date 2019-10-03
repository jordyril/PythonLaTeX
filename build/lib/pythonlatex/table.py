"""
This module modifies the 'Table' class from 'pylatex'
..  :copyright: (c) 2019 by Jordy Rillaerts.
    :license: MIT, see License for more details.
"""

from pylatex import Table as TableOriginal
from pylatex import Package, NoEscape, Tabular
from .saving import LatexSaving
import pandas as pd


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
        LatexSaving.__init__(
            self,
            folder_name=folder_name,
            folder_path=folder_path,
            create_folder=create_folder,
        )
        TableOriginal.__init__(self, *args, position=position, **kwargs)

        self._label = "tbl"

    def _set_tabular(self, tabular, *args, **kwargs):
        """
        TODO
        """
        if isinstance(tabular, Tabular):
            self.tabular = tabular.dumps()

        elif isinstance(tabular, str):
            self.tabular = tabular

        elif isinstance(tabular, pd.DataFrame):
            self.tabular = tabular.to_latex(*args, **kwargs)

    def _tabular_from_df(self, df):
        """
        TODO
        """

        nbr_row, nbr_col = df.shape

        # both have to be increased by 1 for headerrow and index column
        nbr_col += 1
        nbr_row += 1

    def _create_tabular_file(self, filename):
        try:
            self.tabular
        except AttributeError:
            raise AttributeError("No tabular set to save")

        with open(self._absolute_path(f"{filename}.tex"), "w+") as file:
            file.write(self.tabular)

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
    #     with open(self._absolute_path(name + ".tex"), "w") as file:
    #         file.write(to_latex_string)
    #     # self.create_latex_input(name, caption, label, above, **latex_input_kwargs)

    #     return None
