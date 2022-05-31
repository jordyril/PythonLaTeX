"""
This module modifies the 'Table' class from 'pylatex'
..  :copyright: (c) 2019 by Jordy Rillaerts.
    :license: MIT, see License for more details.
"""

from pylatex import Table as TableOriginal
from pylatex import Tabular as TabularOriginal
from pylatex import Package, NoEscape, UnsafeCommand, Command

# from pylatex.base_classes import Arguments
from pylatex.utils import fix_filename
from .saving import LatexSaving
from .float import FloatAdditions
import pandas as pd


class Table(FloatAdditions, LatexSaving, TableOriginal):
    """A class that represents a Table environment with modified methods
    compared to parent TableOriginal
    """

    def __init__(
        self,
        *args,
        folders_path="Latex/",
        outer_folder_name="Tables",
        inner_folder_name="Tabulars",
        position=None,
        **kwargs,
    ):

        LatexSaving.__init__(
            self,
            outer_folder=outer_folder_name,
            inner_folder=inner_folder_name,
            folders_path=folders_path,
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

    def _save_tabular(self, filename):
        try:
            self.tabular
        except AttributeError:
            raise AttributeError("No tabular set to save")

        with open(self._absolute_inner_path(f"{filename}.tex"), "w+") as file:
            file.write(self.tabular)

        return self._relative_inner_path(filename)

    def add_table(
        self,
        tabular,
        filename,
        *args,
        caption=None,
        description=None,
        above=True,
        label=None,
        zref=False,
        placement=NoEscape(r"\centering"),
        adjustbox=True,
        adjustbox_arguments=NoEscape(r"max totalsize={\textwidth}{0.95\textheight}"),
        **kwargs,
    ):
        """Add an image to the figure.
        Args
        ----
        filename: str
            Filename of the image.
        placement: str
            Placement of the table, `None` is also accepted.
        """
        if label is None:
            label = filename

        self._set_tabular(tabular, *args, **kwargs)
        path = self._save_tabular(filename)

        if placement is not None:
            self.append(placement)

        tabular_input = NoEscape(StandAloneTabular(filename=fix_filename(path)).dumps())

        if adjustbox:
            tabular_input = Command(
                command="adjustbox",
                arguments=adjustbox_arguments,
                extra_arguments=tabular_input,
                packages=[Package("adjustbox")],
            )

        self.append(tabular_input)

        if caption is not None:
            self.add_caption_description_label(caption, label, above, description, zref)

    def reset(self):
        self.data = []
        self.tabular = None

    def create_input_latex(
        self,
        tabular,
        filename,
        *args,
        add_table=True,
        caption=None,
        description=None,
        above=True,
        label=None,
        zref=False,
        placement=NoEscape(r"\centering"),
        adjustbox=True,
        adjustbox_arguments=NoEscape(r"max totalsize={\textwidth}{0.95\textheight}"),
        reset=True,
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
        # create automatic caption
        if caption is None:
            caption = filename

        # Allow for no caption
        if caption is False:
            caption = None

        if add_table:
            self.add_table(
                tabular,
                filename,
                *args,
                caption=caption,
                description=description,
                above=above,
                label=label,
                placement=placement,
                adjustbox=adjustbox,
                adjustbox_arguments=adjustbox_arguments,
                **kwargs,
            )
        else:
            self.add_caption_description_label(caption, label, above, description, zref)

        # creating + opening the file
        with open(self._absolute_outer_path(f"{filename}.tex"), "w") as tex_file:
            tex_file.write(self.dumps())

        latex_input = self._print_latex_input(filename)
        self._write_input_to_txt_file(latex_input)

        if reset:
            self.reset()

        return NoEscape(latex_input)


class SubTable(Table):
    """ """

    def __init__(self, width=NoEscape(r"0.49\linewidth"), **kwargs):
        super().__init__(arguments=width, **kwargs)


class StandAloneTabular(UnsafeCommand):
    r"""A class representing a stand alone tabular. (\input{tabularfile})"""

    _latex_name = "input"

    _repr_attributes_mapping = {"filename": "arguments"}

    def __init__(self, filename):
        r"""
        Args
        ----
        filename: str
            The path to the tabular file
        image_options: str or `list`
            Specifies the options for the image (ie. height, width)
        """

        arguments = [NoEscape(filename)]

        super().__init__(command=self._latex_name, arguments=arguments)
