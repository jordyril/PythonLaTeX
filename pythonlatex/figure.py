"""The module modifies the 'Figure' class from 'pylatex'.

..  :copyright: (c) 2019 by Jordy Rillaerts.
    :license: MIT, see License for more details.
"""

from pathlib import Path
from typing import ClassVar

import matplotlib.pyplot as plt
from pylatex import Command, NoEscape, Package, StandAloneGraphic
from pylatex import Figure as FigureOriginal

from pythonlatex.float import FloatAdditions
from pythonlatex.saving import LatexSaving


class Figure(FloatAdditions, LatexSaving, FigureOriginal):
    """A class representing a Figure with modified methods compared to parent."""

    def __init__(
        self,
        *args: tuple,
        folders_path: str = "Latex/",
        outer_folder_name: str = "Figures",
        inner_folder_name: str = "Graphics",
        position: str | None = None,
        **kwargs: tuple,
    ) -> None:
        """Initialize a Figure instance with custom folder paths and position.

        Args:
            folders_path: Base path for saving LaTeX files and figures
            outer_folder_name: Name of the outer folder for figure files
            inner_folder_name: Name of the inner folder for graphics
            position: Optional position argument for the figure
            *args: Additional positional arguments passed to parent class
            **kwargs: Additional keyword arguments passed to parent class

        """
        LatexSaving.__init__(
            self,
            outer_folder=outer_folder_name,
            inner_folder=inner_folder_name,
            folders_path=folders_path,
        )
        FigureOriginal.__init__(self, *args, position=position, **kwargs)

        self._label = "fig"

    def save_plot(
        self,
        filename: str,
        *args: tuple,
        extension: str = "png",
        **kwargs: tuple,
    ) -> str:
        """Save the plot in the 'inner' folder.

        Args:
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

        Returns:
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
        filename: str,
        *args: tuple,
        caption: str | None = None,
        description: str | None = None,
        above: bool = True,
        label: str | None = None,
        zref: bool = False,
        resizebox: bool = False,
        resizebox_arguments: tuple | None = None,
        width: str | None = None,
        placement: str | None = None,
        extension: str = "png",
        **kwargs: tuple,
    ) -> None:
        """Add the current Matplotlib plot to the figure.

        The plot that gets added is the one that would normally be shown when
        using ``plt.show()``. Replaced feature of random temp saving with
        dedicated filename saving compared to original package.

        Args:
        ----
        filename: Name of the figure for saving.
        args: Arguments passed to plt.savefig for displaying the plot.
        caption: Optional caption to be added to the figure.
        description: Optional description text for the figure.
        above: In case caption is given, position of caption can be above or below figure.
        label: Optional label for referencing the figure.
        zref: Whether to use zref package for referencing.
        resizebox: Whether to apply resizebox command to the figure.
        resizebox_arguments: Arguments for the resizebox command.
        width: Width of the figure in LaTeX terms.
        placement: Placement command for the figure.
        extension: Extension of image file indicating figure file type.
        kwargs: Keyword arguments passed to plt.savefig for displaying the plot.

        """
        # Set default values for NoEscape parameters
        if resizebox_arguments is None:
            resizebox_arguments = (NoEscape(r"\columnwidth"), NoEscape("!"))
        if width is None:
            width = NoEscape(r"0.8\textwidth")
        if placement is None:
            placement = NoEscape(r"\centering")

        label, caption = self._check_label_caption(label, caption, filename)

        path = self.save_plot(filename, *args, extension=extension, **kwargs)

        if placement is not None:
            self.append(placement)

        if width is not None:
            width = "width=" + str(width)

        graphic = StandAloneGraphic(image_options=width, filename=path)

        if resizebox:
            figure_input = Command(
                command="resizebox",
                arguments=resizebox_arguments,
                extra_arguments=graphic,
                packages=[Package("graphics")],
            )
        else:
            figure_input = graphic

        self.append(figure_input)

        if caption is not None:
            self.add_caption_description_label(caption, label, above, description, zref)

    def reset(
        self,
        show: bool = True,
        close: bool = False,
        *args: tuple,
        **kwargs: tuple,
    ) -> None:
        """Reset the Figure instance.

        This way the same set-up can be used for following figures,
        without having to create a Figure instance with the same path,
        folder and extension option every time.

        Args:
        ----
        show: bool
            If set to True, plt.show() will be called. Default is True.
        close: bool
            If set to True, plt.close() will be called. Default is False.
        args:
            Arguments passed to plt.show or plt.close.
        kwargs:
            Keyword arguments passed to plt.show or plt.close.

        """
        if show:
            plt.show(*args, **kwargs)

        if close:
            plt.close()

        self.data = []

    def create_input_latex(
        self,
        filename: str,
        *args: tuple,
        add_plot: bool = True,
        caption: str | None = None,
        description: str | None = None,
        above: bool = True,
        label: str | None = None,
        zref: bool = False,
        printing_input: bool = True,
        resizebox: bool = False,
        resizebox_arguments: tuple | None = None,
        width: str | None = None,
        placement: str | None = None,
        **kwargs: tuple,
    ) -> None:
        """Create separate input tex-file that can be used to input Figure.

        Args:
        ----
        filename: Name of the plot for saving.
        args: Arguments passed to plt.savefig for displaying the plot.
        add_plot: In case of normal figure this is True, in case of subfigure,
            no new figure needs to be added so this option should be set to False.
        caption: Optional caption to be added to the figure.
        description: Optional description text for the figure.
        above: In case caption is given, position of caption can be above or below figure.
        label: Optional label for referencing the figure.
        zref: Whether to use zref package for referencing.
        printing_input: Whether to print the LaTeX input to console.
        resizebox: Whether to apply resizebox command to the figure.
        resizebox_arguments: Arguments for the resizebox command.
        width: Width of the figure in LaTeX terms.
        placement: Placement command for the figure.
        kwargs: Keyword arguments passed to plt.savefig for displaying the plot.

        """
        # Set default values for NoEscape parameters
        if resizebox_arguments is None:
            resizebox_arguments = (NoEscape(r"\columnwidth"), NoEscape("!"))
        if width is None:
            width = NoEscape(r"0.8\textwidth")
        if placement is None:
            placement = NoEscape(r"\centering")

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
                resizebox=resizebox,
                resizebox_arguments=resizebox_arguments,
                width=width,
                placement=placement,
                **kwargs,
            )
        else:
            self.add_caption_description_label(caption, label, above, description, zref)

        # creating + opening the final input file in the 'outer' folder
        with Path(f"{self._absolute_outer_path(filename)}.tex").open("w+") as tex_file:
            tex_file.write(self.dumps())

        latex_input = self._input_lines(filename)
        self._write_input_to_txt_file(latex_input)

        if printing_input:
            print(latex_input)

    def _check_label_caption(
        self,
        label: str | None,
        caption: str | bool | None,
        filename: str,
    ) -> tuple[str | None, str | None]:
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

    Methods are almost exact copy of original pylatex package.
    """

    packages: ClassVar[list] = [Package("subcaption")]

    #: By default a subfigure is not on its own paragraph since that looks
    #: weird inside another figure.
    separate_paragraph: bool = False

    _repr_attributes_mapping: ClassVar[dict] = {"width": "arguments"}

    def __init__(self, width: str | None = None, **kwargs: dict) -> None:
        """Initialize a SubFigure instance.

        Args:
        ----
        width: Width of the subfigure itself. It needs a width because it is
            inside another figure.
        **kwargs: Additional keyword arguments passed to the parent Figure class.

        """
        if width is None:
            width = NoEscape(r"0.49\linewidth")
        super().__init__(arguments=width, **kwargs)

    def add_image(
        self,
        filename: str,
        *,
        width: str | None = None,
        placement: str | None = None,
    ) -> None:
        """Add an image to the subfigure.

        Args:
        ----
        filename: Filename of the image.
        width: Width of the image in LaTeX terms.
        placement: Placement of the figure, `None` is also accepted.

        """
        if width is None:
            width = NoEscape(r"\linewidth")
        super().add_image(filename, width=width, placement=placement)
