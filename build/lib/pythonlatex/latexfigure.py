"""
This module modifies the 'Figure' class from 'pylatex'
..  :copyright: (c) 2019 by Jordy Rillaerts.
    :license: MIT, see License for more details.
"""

from pylatex import Figure
from .latexsaving import LatexSaving
import os
import posixpath

# - TRYING INHERITANCE


class LatexFigure(LatexSaving, Figure):
    """A class that represents a Figure environment with modified methods compared to parent"""

    def __init__(
        self,
        folder_path="Latex/",
        folder_name="Folder",
        create_folder=True,
        position=None,
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
        Figure.__init__(self, position=position)
        # print("figure init out")

    def test(self):
        print("test")

    def _save_plot(self, filename, *args, extension="jpg", **kwargs):
        filepath = posixpath.join(self._folder, filename)

        # plt.savefig(filepath, *args, **kwargs)
        return filepath


# TRYING COMPOSITION
