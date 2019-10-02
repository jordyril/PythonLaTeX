"""
This module modifies the 'Figure' class from 'pylatex'
..  :copyright: (c) 2019 by Jordy Rillaerts.
    :license: MIT, see License for more details.
"""

from pylatex import Figure as FigureOriginal
from pylatex import Package, NoEscape, Command
from .saving import LatexSaving
import matplotlib.pyplot as plt


class Figure(LatexSaving, FigureOriginal):
    """A class that represents a Figure environment with modified methods compared to parent"""

    def __init__(
        self,
        *args,
        folder_path="Latex/",
        folder_name="Figures",
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
        FigureOriginal.__init__(self, *args, position=position, **kwargs)
        # print("figure init out")
        self._label = "fig"

    def _save_plot(self, filename, *args, extension="jpg", **kwargs):
        """Save the plot.
        Args
        ----
        filename: str
            Name of the figure for saving
        args:
            Arguments passed to plt.savefig for displaying the plot.
        extension : str
            extension of image file indicating figure file type
        kwargs:
            Keyword arguments passed to plt.savefig for displaying the plot. In
            case these contain ``width`` or ``placement``, they will be used
            for the same purpose as in the add_image command. Namely the width
            and placement of the generated plot in the LaTeX document.
        Returns
        -------
        str
            The relative path/name with which the plot has been saved.
            (original package stored figure in temp directory, here the naming is added
            and it is being saved in a known directory)
        """
        name = f"{filename}.{extension}"
        plt.savefig(self._absolute_path(name), *args, **kwargs)
        return self._relative_path(name)

    def add_plot(
        self,
        filename,
        *args,
        caption=None,
        above=True,
        label=None,
        extension="jpg",
        **kwargs,
    ):
        """Add the current Matplotlib plot to the figure.
        The plot that gets added is the one that would normally be shown when
        using ``plt.show()``. Replaced feature of random temp saving with dedicated filename saving
        compared to original package
        Args
        ----
        filename: str
            Name of the figure for saving
        args:
            Arguments passed to plt.savefig for displaying the plot.
        caption: : str
            Optional caption to be added to the figure
        above: bool
            In case caption is given, position of caption can be above or bellow figure
        extension : str
            Extension of image file indicating figure file type
        kwargs:
            Keyword arguments passed to plt.savefig for displaying the plot. In
            case these contain ``width`` or ``placement``, they will be used
            for the same purpose as in the add_image command. Namely the width
            and placement of the generated plot in the LaTeX document.
        """
        if label is None:
            label = filename

        add_image_kwargs = {}

        for key in ("width", "placement"):
            if key in kwargs:
                add_image_kwargs[key] = kwargs.pop(key)

        path = self._save_plot(filename, *args, extension=extension, **kwargs)

        # if (caption is not None) and above:
        #     self.add_caption_label(caption, label)

        self.add_image(path, **add_image_kwargs)

        if caption is not None:
            self.add_caption_label(caption, label, above)

        # if (caption is not None) and (not above):
        #     self.add_caption_label(caption, label)

    def reset(self, show=True, close=False, *args, **kwargs):
        """Resets the Figure instance, this way the same set-up
        can be used for following figures without having to create
        a Figure instance with the same path, folder and extension option every time
                Args
        ----
        close: bool
            if set to True, plt.close() will be called for. Default is False
        args:
            Arguments passed to plt.close.
        kwargs:
            Keyword arguments passed to plt.close for displaying the plot.
        """
        if show:
            plt.show(*args, **kwargs)

        if close:
            plt.close()

        self.data = []

    def write_input_latex(
        self,
        filename,
        *args,
        add_plot=True,
        caption=None,
        above=True,
        label=None,
        **kwargs,
    ):
        """Creates separate input tex-file that can be used to input figure
        Args
        ----
        filename: str
            Name of the figure for saving
        args:
            Arguments passed to plt.savefig for displaying the plot.
        add_plot: bool
            In case of normal figure this is True, in case of subfigure, no new figure needs
            to be added so this option should be set to False
        caption: str
            Optional caption to be added to the figure
        above: bool
            In case caption is given, position of caption can be above or bellow figure
        extension : str
            Extension of image file indicating figure file type
        kwargs:
            Keyword arguments passed to plt.savefig for displaying the plot. In
            case these contain ``width`` or ``placement``, they will be used
            for the same purpose as in the add_image command. Namely the width
            and placement of the generated plot in the LaTeX document.
        """
        if add_plot:
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

    def add_caption(self, caption, above=True):
        """Add a caption to the float.
        Args
        ----
        caption: str
            The text of the caption.
        above: bool
            Position of caption
        """
        if above:
            self.insert(0, Command("caption", caption))

        else:
            self.append(Command("caption", caption))

    def add_label(self, label, above=True):
        self.packages.add(Package("zref-user"))
        if above:
            self.insert(0, Command("zlabel", NoEscape(f"{self._label}:{label}")))
        else:
            self.append(Command("zlabel", NoEscape(f"{self._label}:{label}")))

    def add_caption_label(self, caption, label, above=True):
        if above:
            # note that we do label first here, so in final label is after caption
            self.add_label(NoEscape(label), above)
            self.add_caption(caption, above)
        else:
            self.add_caption(caption, above)
            self.add_label(NoEscape(label), above)


class SubFigure(Figure):
    """A class that represents a subfigure from the subcaption package.
    Methods are almost exact copy of original pylatex package"""

    packages = [Package("subcaption")]

    #: By default a subfigure is not on its own paragraph since that looks
    #: weird inside another figure.
    separate_paragraph = False

    _repr_attributes_mapping = {"width": "arguments"}

    def __init__(self, width=NoEscape(r"0.45\linewidth"), **kwargs):
        """
        Args
        ----
        width: str
            Width of the subfigure itself. It needs a width because it is
            inside another figure.
        """

        super().__init__(arguments=width, **kwargs)

    def add_image(self, filename, *, width=NoEscape(r"\linewidth"), placement=None):
        """Add an image to the subfigure.
        Args
        ----
        filename: str
            Filename of the image.
        width: str
            Width of the image in LaTeX terms.
        placement: str
            Placement of the figure, `None` is also accepted.
        """

        super().add_image(filename, width=width, placement=placement)
