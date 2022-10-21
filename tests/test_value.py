from pythonlatex import Value
from pylatex import Document, NoEscape

import unittest

# import os
import shutil

try:
    shutil.rmtree("Latex")
except FileNotFoundError:
    pass


class Testvalues(unittest.TestCase):
    def test_path(self):
        path = "./Latex/test_path/"
        value = Value(folders_path=path)
        self.assertEqual(value._folders_path, path)

    def test_outer_folder(self):
        folder = "Outer_test"
        value = Value(outer_folder_name=folder)

        self.assertEqual(value._outer_folder_name, folder)

    def test_texinput(self):
        value = Value()
        name = "test_tex"
        input_tex = value.create_input_latex("1", name)

        # create document for testing input statement
        doc = Document()
        doc.dumps()
        doc.append(input_tex)
        doc.preamble.append(NoEscape(r"\usepackage{booktabs}"))
        doc.preamble.append(NoEscape(r"\usepackage{zref-user}"))
        doc.preamble.append(NoEscape(r"\usepackage{adjustbox}"))

        doc.generate_pdf(f"Latex/{name}", clean_tex=False)

    def test_texinput2(self):
        value = Value()
        name = "test_tex"
        input_tex = value("1", name)

        # create document for testing input statement
        doc = Document()
        doc.dumps()
        doc.append(input_tex)
        doc.preamble.append(NoEscape(r"\usepackage{booktabs}"))
        doc.preamble.append(NoEscape(r"\usepackage{zref-user}"))
        doc.preamble.append(NoEscape(r"\usepackage{adjustbox}"))

        doc.generate_pdf(f"Latex/{name}", clean_tex=False)


if __name__ == "__main__":
    unittest.main()
