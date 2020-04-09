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
