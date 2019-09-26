# =============================================================================
# PACKAGES
# =============================================================================
import os
import matplotlib.pyplot as plt

# =============================================================================
# MAIN LATEX
# =============================================================================


class Latex(object):
    """
    Class for my standardised formats
    """

    def __init__(self, folder_path="."):
        self._folder_path = folder_path
        self.create_subfolder()
        self._extension = ".tex"

    def create_latex_input(self):
        pass

    def _folder(self):
        return f"{self._folder_path}/{self.__str__()}s"

    @property
    def _absolute_path(self):
        path = f"{self._folder()}/"
        return path

    @property
    def _relative_path(self):
        path = f"{self.__str__()}s/"
        return path

    def create_subfolder(self):
        if not os.path.exists(self._folder()):
            os.makedirs(self._folder())


# =============================================================================
# LATEX TABLE
# =============================================================================
class LatexFloats(Latex):
    def __init__(self, folder_path=".", float_position="p"):

        Latex.__init__(self, folder_path)

        self.float_position = float_position
        self._create_inputs_folder()
        self._create_input_txt_file()

    def _caption_label(self, file, caption, label):
        file.write("\\caption{" + caption + "}\n")
        # file.write("\\label{" + self._prefixlabel + label + "}\n")
        file.write("\\zlabel{" + self._prefixlabel + label + "}\n")
        return None

    def _begin_object(self, input_tex):
        input_tex.write("\\begin{" + self._object + "}[" + self.float_position + "]\n")
        input_tex.write("\\center\n")

    def _end_object(self, input_tex):
        input_tex.write("\\end{" + self._object + "}")

    def _print_latex_input(self, filename):
        to_print = (
            f"\n %Latex {self._object} input: {filename} %\n"
            f"\\input{{Inputs/input_{filename}}} \n"
        )

        # to_print = """
        # \n% Latex " + self._object + " input: " + filename + " %\n
        # \\input{Inputs/input_" + filename + "}
        # """
        print(to_print)
        # print("\n% Latex " + self._object + " input: " + filename + " %")
        # print("\\input{Inputs/input_" + filename + "}")
        return to_print

    def _create_inputs_folder(self):
        if not os.path.exists(f"{self._folder_path}/Inputs"):
            os.makedirs(f"{self._folder_path}/Inputs")

    @property
    def _inputs_folder(self):
        return f"{self._folder_path}/Inputs"

    def write_input_to_text(self, latex_input):
        with open(f"{self._inputs_folder}/inputs.txt", "a") as file:
            file.write(latex_input)

    def _create_input_txt_file(self):
        with open(f"{self._inputs_folder}/inputs.txt", "w") as file:
            text = "Summary of all Inputs".upper()
            n = len(text)
            file.write(f"{n * '='} \n")
            file.write(f"{text} \n")
            file.write(f"{n * '='} \n")


class LatexTable(LatexFloats):
    def __init__(self, folder_path=".", float_position="p"):
        LatexFloats.__init__(self, folder_path, float_position)

        self._prefix = "table_"
        self._prefixlabel = "tbl: "
        self._object = "table"

    def __str__(self):
        return "Table"

    def VCV(
        self, vcv, name, caption, label=None, rounding=2, above=True, latex_input=True
    ):
        columns = vcv.shape[1]

        prefix = "vcv_"

        # prepare standard format
        col_form = "l|" + columns * "r"
        fl_form = "%." + str(rounding) + "f"

        # Transfer to latex file
        vcv.to_latex(
            self._relative_path + prefix + name + self._extension,
            float_format=fl_form,
            column_format=col_form,
        )

        if latex_input:
            self.create_latex_input(prefix + name, caption, label, above)

        return None

    def Sharpe_ratio_table(
        self,
        table,
        name,
        caption,
        label=None,
        percentage_points=False,
        rounding=2,
        above=True,
        latex_input=True,
    ):
        prefix = "sharpe_"
        columns = table.shape[1]

        copy = table.copy()
        formatting1 = "{:,." + str(rounding) + "f}%"
        formatting2 = "{:,." + str(rounding + 1) + "f}"

        if not percentage_points:
            copy.loc["Mean"] = copy.loc["Mean"] * 100
            copy.loc["Volatility"] = copy.loc["Volatility"] * 100

        copy.loc["Mean"] = copy.loc["Mean"].map(formatting1.format)
        copy.loc["Volatility"] = copy.loc["Volatility"].map(formatting1.format)
        copy.loc["Sharpe ratio"] = copy.loc["Sharpe ratio"].map(formatting2.format)

        # prepare standard format
        col_form = "l|" + columns * "r"

        # Transfer to latex file
        copy.to_latex(
            self._relative_path + prefix + name + self._extension,
            column_format=col_form,
        )

        if latex_input:
            self.create_latex_input(prefix + name, caption, label, above)

        return None

    def to_latex(
        self, table, name, caption, label=None, rounding=2, above=True, **latex_kwargs
    ):
        """
        see:
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_latex.html
        for the possible kwargs
        """
        try:
            to_latex_kwargs = latex_kwargs["to_latex"]

        except KeyError:
            to_latex_kwargs = {}

        # Escape math
        try:
            to_latex_kwargs["escape"]
        except KeyError:
            to_latex_kwargs["escape"] = False

        try:
            latex_input_kwargs = latex_kwargs["input"]

        except KeyError:
            latex_input_kwargs = {}

        self.create_tabular_file(table, name, rounding, **to_latex_kwargs)

        self.create_latex_input(name, caption, label, above, **latex_input_kwargs)

        return None

    def create_latex_input(
        self,
        filename,
        caption,
        label=None,
        above=True,
        adjustbox=("\\textwidth", "0.95\\textheight"),
    ):
        """
        Creates input line to be copied into latex s.t. tables and figures
        will automatically be imported in latex with given title and label
        """
        # creating label
        if label is None:
            label = filename

        # creating + opening the file
        input_tex = open(
            os.path.join(self._inputs_folder, "input_" + filename + self._extension),
            "w",
        )

        # begin object
        self._begin_object(input_tex)

        # Caption and label above
        if above:
            self._caption_label(input_tex, caption, label)

        # adjustbox print - begin
        input_tex.write(
            "\\adjustbox{max totalsize={"
            + adjustbox[0]
            + "}{"
            + adjustbox[1]
            + "}}{ \n"
        )

        # import
        input_tex.write("\\input{" + self._relative_path + filename + "}\n")

        # adjustbox print - end
        input_tex.write("}\n")

        # Caption and label bellow
        if not above:
            self._caption_label(input_tex, caption, label)

        # end object
        self._end_object(input_tex)

        # closing the file
        input_tex.close()

        latex_input = self._print_latex_input(filename)

        self.write_input_to_text(latex_input)
        return latex_input

    def subtables(
        self,
        filename,
        subtables,
        caption,
        subcaptions,
        label=None,
        sublabels=None,
        above=True,
        subabove=True,
        lw=0.45,
    ):

        input_tex = open(
            os.path.join(self._inputs_folder, "input_" + filename + self._extension),
            "w",
        )
        # create label
        if label is None:
            label = filename
        # create sublables
        if sublabels is None:
            sublabels = subtables

        # begin object
        self._begin_object(input_tex)

        # Caption and label above
        if above:
            self._caption_label(input_tex, caption, label)

        #
        # loop over tables
        for tbl, cap, lbl in zip(subtables, subcaptions, sublabels):
            input_tex.write("\\begin{subtable}[t]{" + str(lw) + "\linewidth}\n")

            # Caption and label above
            if subabove:
                self._caption_label(input_tex, cap, lbl)

            input_tex.write("\\input{" + self._relative_path + tbl + "}\n")

            # Caption and label bellow
            if not subabove:
                self._caption_label(input_tex, cap, lbl)

            input_tex.write("\\end{subtable}\\hfill\n")

        # Caption and label bellow
        if not above:
            self._caption_label(input_tex, caption, label)

        # end object
        input_tex.write("\\end{table}")

        # closing the file
        input_tex.close()

        print("\n% Latex table input: " + filename + " %")
        print("\\input{Inputs/input_" + filename + "}")

        return None

    def create_tabular_file(self, table, name, rounding=2, **to_latex_kwargs):
        # columns
        columns = table.shape[1]

        # Escape math
        try:
            to_latex_kwargs["escape"]
        except KeyError:
            to_latex_kwargs["escape"] = True

        ## Standard formats
        # columns
        try:
            to_latex_kwargs["column_format"]
        except KeyError:
            to_latex_kwargs["column_format"] = "l|" + columns * "r"

        # floats
        try:
            to_latex_kwargs["float_format"]
        except KeyError:
            to_latex_kwargs["float_format"] = "%." + str(rounding) + "f"

        # Transfer to latex file
        table.to_latex(self._relative_path + name + self._extension, **to_latex_kwargs)

    def _print_tabular_input(self, name):
        print("\n% Latex tabular input: " + name + " %")
        print("\\input{Tables/" + name + "}")
        return None

    def create_tabular_input(self, table, name, rounding=2, **to_latex_kwargs):
        self.create_tabular_file(table, name, rounding, **to_latex_kwargs)
        self._print_tabular_input(name)
        return None

    def input_from_to_latex_string(
        self,
        to_latex_string,
        name,
        caption,
        label=None,
        above=True,
        **latex_input_kwargs,
    ):
        # write to_latex_tabular to .tex file - create tabular file
        with open(self._absolute_path + name + self._extension, "w") as file:
            file.write(to_latex_string)
        self.create_latex_input(name, caption, label, above, **latex_input_kwargs)

        return None


# =============================================================================
# LATEX FIGURE
# =============================================================================
class LatexFigure(LatexFloats):
    def __init__(self, folder_path=".", extension="jpg", float_position="p"):
        LatexFloats.__init__(self, folder_path, float_position)

        self._prefixlabel = "fig: "
        self._object = "figure"
        self._figextension = "." + extension

    @property
    def extension(self):
        return self._figextension

    def __str__(self):
        return "Figure"

    def to_latex(self, filename, caption, label=None, above=True):
        """
        Creates input line to be copied into latex s.t. tables and figures
        will automatically be imported in latex with given title
        """
        # creating label
        if label is None:
            label = filename

        # creating + opening the file
        input_tex = open(
            os.path.join(self._inputs_folder, "input_" + filename + ".tex"), "w"
        )

        # begin object
        self._begin_object(input_tex)

        # Caption and label above
        if above:
            self._caption_label(input_tex, caption, label)

        # Import
        input_tex.write(
            "\\includegraphics[scale=0.8]{"
            + self._relative_path
            + filename
            + self._figextension
            + "}\n"
        )

        # Caption and label bellow
        if not above:
            self._caption_label(input_tex, caption, label)

        # end object
        self._end_object(input_tex)

        # closing the file
        input_tex.close()

        latex_input = self._print_latex_input(filename)
        self.write_input_to_text(latex_input)
        return latex_input

    def subfigure(
        self,
        filename,
        subfigures,
        caption,
        subcaptions,
        label=None,
        sublabels=None,
        above=True,
        subabove=True,
        lw=0.49,
    ):

        # Open and create file
        input_tex = open(
            os.path.join(self._inputs_folder, "input_" + filename + self._extension),
            "w",
        )
        # create label
        if label is None:
            label = filename

        # create sublables
        if sublabels is None:
            sublabels = subfigures

        # begin object
        self._begin_object(input_tex)

        # Caption and label above
        if above:
            self._caption_label(input_tex, caption, label)

        # loop over tables
        for fig, cap, lbl in zip(subfigures, subcaptions, sublabels):
            input_tex.write("\\begin{subfigure}[h]{" + str(lw) + "\linewidth}\n")

            # Caption and label above
            if subabove:
                self._caption_label(input_tex, cap, lbl)

            input_tex.write(
                "\includegraphics[width=\\textwidth]{"
                + self._relative_path
                + fig
                + self._figextension
                + "}\n"
            )

            # Caption and label bellow
            if not subabove:
                self._caption_label(input_tex, cap, lbl)

            input_tex.write("\\end{subfigure}\\hfill\n")

        # Caption and label bellow
        if not above:
            self._caption_label(input_tex, caption, label)
        #
        # end object
        self._end_object(input_tex)

        # closing the file
        input_tex.close()

        latex_input = self._print_latex_input(filename)
        self.write_input_to_text(latex_input)
        return latex_input

    @property
    def savefig_path(self):
        return self._absolute_path

    def savefig(self, name, **kwargs):
        plt.savefig(f"{self.savefig_path}{name}{self.extension}", **kwargs)
        return None


# =============================================================================
# LATEX VALUE
# =============================================================================
class LatexValue(Latex):
    def __init__(self, folder_path="."):
        Latex.__init__(self, folder_path)

        self._object = "value"

    def __str__(self):
        return "Value"

    def to_latex(self, value, name, rounding=2):
        if not isinstance(value, str):
            value = ("{:0." + str(rounding) + "f}").format(value)

        value = value + "%"  # otherwise extra space after \input{}
        path_filename_extension = self._absolute_path + name + ".tex"
        tex_file = open(path_filename_extension, "w+")
        tex_file.write(value)
        tex_file.close()

        print("\n% Latex Value input: " + name + " %")
        print("\\input{" + self._relative_path + name + "}")

        return None
