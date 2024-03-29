"""
This module modifies the 'Figure' class from 'pylatex'
..  :copyright: (c) 2019 by Jordy Rillaerts.
    :license: MIT, see License for more details.
"""

from pylatex import NoEscape
from .saving import LatexSaving
from numpy import round


class Value(LatexSaving):
    """A class that represents a Value"""

    def __init__(
        self,
        folders_path="Latex/",
        outer_folder_name="Values",
    ):

        LatexSaving.__init__(
            self,
            outer_folder=outer_folder_name,
            inner_folder=outer_folder_name,
            folders_path=folders_path,
        )

    def create_input_latex(
        self, value, filename, printing_input=True, rounding=None, vformat=None
    ):
        """Creates separate input tex-file that can be used to input tabular within table environment
        Args
        ----
        filename: str
            Name of the table for saving
        value: float, int, str
            value that will be saved into separate tex file
        args:
            Arguments passed to pd.df.to_latex for displaying the tabular.
        kwargs:
            Keyword arguments passed to plt.savefig for displaying the plot.
        """

        if not isinstance(value, str):
            if isinstance(value, int):
                value = str(value)
            else:
                if vformat:
                    value = f"{{{vformat}}}".format(value)
                elif rounding:
                    value = str(round(value, rounding))
                else:
                    raise ValueError(
                        "Value should be of type int or string, if float a rounding or format needs to be provided"
                    )

        # creating + opening the file
        with open(self._absolute_outer_path(f"{filename}.tex"), "w") as tex_file:
            tex_file.write(value)
            tex_file.write("%")

        latex_input = self._input_lines(filename)
        self._write_input_to_txt_file(latex_input)

        if printing_input:
            print(latex_input)
        return None
        # return NoEscape(latex_input)

    def __call__(
        self, value, filename, printing_input=True, rounding=None, vformat=None
    ):
        self.create_input_latex(value, filename, printing_input, rounding, vformat)
