"""
This module modifies the 'Figure' class from 'pylatex'
..  :copyright: (c) 2019 by Jordy Rillaerts.
    :license: MIT, see License for more details.
"""

from pylatex import Figure as FigureOriginal
from pylatex import Package, NoEscape, Command, Package
from .saving import LatexSaving
from .float import FloatAdditions
import matplotlib.pyplot as plt


class Figure(FloatAdditions, LatexSaving, FigureOriginal):
    """A class that represents a Figure environment with modified methods compared to parent"""

    def __init__(
        self,
        *args,
        folders_path="Latex/",
        outer_folder_name="Figures",
        inner_folder_name="Graphics",
        position=None,
        **kwargs,
    ):
        LatexSaving.__init__(
            self,
            outer_folder=outer_folder_name,
            inner_folder=inner_folder_name,
            folders_path=folders_path,
        )
        FigureOriginal.__init__(self, *args, position=position, **kwargs)

        self._label = "fig"

    def save_plot(self, filename, *args, extension="png", **kwargs):
        """Saves the plot in the 'inner' folder
        Args
        ----
        filename: str
            Name of the plot for saving
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
        plt.savefig(*args, fname=self._absolute_inner_path(name), **kwargs)
        return self._relative_inner_path(name)

    def add_plot(
        self,
        filename,
        *args,
        caption=None,
        description=None,
        above=True,
        label=None,
        zref=False,
        resizebox=False,
        resizebox_arguments=(NoEscape(r"\columnwidth"), NoEscape("!")),
        extension="png",
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
        label, caption = self._check_label_caption(label, caption, filename)

        add_image_kwargs = {}

        for key in ("width", "placement"):
            if key in kwargs:
                add_image_kwargs[key] = kwargs.pop(key)

        path = self.save_plot(filename, *args, extension=extension, **kwargs)


        graphics = self.add_image(path, **add_image_kwargs)

        if resizebox:
            figure_input = Command(
                command="resizebox",
                arguments=resizebox_arguments,
                extra_arguments=graphics,
                packages=[Package("graphics")],
            )

        self.append(figure_input)
        

        if caption is not None:
            self.add_caption_description_label(caption, label, above, description, zref)

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

    def create_input_latex(
        self,
        filename,
        *args,
        add_plot=True,
        caption=None,
        description=None,
        above=True,
        label=None,
        zref=False,
        printing_input=True,
        **kwargs,
    ):
        """Creates separate input tex-file that can be used to input Figure
        Args
        ----
        filename: str
            Name of the plot for saving
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
        label, caption = self._check_label_caption(label, caption, filename)

        if add_plot:
            self.add_plot(
                filename,
                *args,
                caption=caption,
                above=above,
                label=label,
                description=description,
                zref=zref,
                **kwargs,
            )
        else:
            self.add_caption_description_label(caption, label, above, description, zref)

        # creating + opening the final input file in the 'outer' folder
        with open(f"{self._absolute_outer_path(filename)}.tex", "w+") as tex_file:
            tex_file.write(self.dumps())

        latex_input = self._input_lines(filename)
        self._write_input_to_txt_file(latex_input)

        if printing_input:
            print(latex_input)
        return None
        # return NoEscape(latex_input)

    def _check_label_caption(self, label, caption, filename):
        if label is None:
            label = filename

        # create automatic caption
        if caption is None:
            caption = filename

        # Allow for  no caption
        if caption is False:
            caption = None

        return label, caption


class SubFigure(Figure):
    """A class that represents a subfigure from the subcaption package.
    Methods are almost exact copy of original pylatex package"""

    packages = [Package("subcaption")]

    #: By default a subfigure is not on its own paragraph since that looks
    #: weird inside another figure.
    separate_paragraph = False

    _repr_attributes_mapping = {"width": "arguments"}

    def __init__(self, width=NoEscape(r"0.49\linewidth"), **kwargs):
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
