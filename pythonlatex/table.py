"""
This module modifies the 'Table' class from 'pylatex'
..  :copyright: (c) 2019 by Jordy Rillaerts.
    :license: MIT, see License for more details.
"""

from pylatex import Table as TableOriginal
from pylatex import Tabular as TabularOriginal
from pylatex import Package, NoEscape
from .saving import LatexSaving
import pandas as pd


class Tabular(LatexSaving, TabularOriginal):
    """
    TODO
    """

    def __init__(self):
        pass


class Table(LatexSaving, TableOriginal):
    """A class that represents a Table environment with modified methods compared to parent"""

    def __init__(
        self,
        *args,
        folder_path="Latex/",
        folder_name="Tabulars",
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
        if isinstance(tabular, TabularOriginal):
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

    def create_input_latex(
        self,
        filename,
        tabular,
        *args,
        add_table=True,
        caption=None,
        above=True,
        label=None,
        **kwargs,
    ):
        """Creates separate input tex-file that can be used to input tabular within table environment
        Args
        ----
        filename: str
            Name of the table for saving
        tabular: str, pandas.DataFrame, Tabular
            tabular that will be saved and created into a proper table
        args:
            Arguments passed to pd.df.to_latex for displaying the tabular.
        add_table: bool
            In case of normal table this is True, in case of subtable, no new table needs
            to be added so this option should be set to False
        caption: str
            Optional caption to be added to the table
        above: bool
            In case caption is given, position of caption can be above or bellow table
        extension : str
            Extension of image file indicating table file type
        kwargs:
            Keyword arguments passed to plt.savefig for displaying the plot.
        """
        if add_table:
            self.add_plot(
                filename, *args, caption=caption, above=above, label=label, **kwargs
            )
        else:
            self.add_caption_label(caption, label, above)

        # creating + opening the file
        with open(f"{self._inputs_folder}input_{filename}.tex", "w") as tex_file:
            tex_file.write(self.dumps())

        latex_input = self._print_latex_input(filename)
        self._write_input_to_txt_file(latex_input)

        return NoEscape(latex_input)

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
