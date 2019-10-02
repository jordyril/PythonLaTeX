# import numpy as np
from pythonlatex import Table

# from pylatex import Document, NoEscape

import unittest

# import os
import shutil

try:
    shutil.rmtree("Latex")
except FileNotFoundError:
    pass


class TestTables(unittest.TestCase):
    def test_path(self):
        path = "./test"
        fig = Table(folder_path=path, create_folder=False)
        self.assertEqual(fig._folder_path, path)

    def test_folder(self):
        folder = "test_folder"
        fig = Table(folder_name=folder, create_folder=False)

        self.assertEqual(fig._folder_name, folder)

    def test_position(self):
        position = "h"
        fig = Table(position=position, create_folder=False)
        self.assertEqual(fig.options, position)

    # def test_reset(self):
    #     fig = Table()
    #     # Table 1
    #     for i in range(1, 3):
    #         name = f"test{i}"
    #         plt.Table()
    #         plt.plot(x, y, label=i)
    #         fig.add_plot(name)

    #         # check if correct latex output is produced
    #         self.assertEqual(
    #             fig.dumps(),
    #             (
    #                 f"\\begin{{Table}}%\n\\centering%\n\\includegraphics[width=0.8\\textwidth]"
    #                 + f"{{Tables/test{i}.jpg}}%\n\\end{{Table}}"
    #             ),
    #         )
    #         fig.reset(close=True)

    # def test_texinput(self):
    #     fig = Table()
    #     name = "test_tex"
    #     caption = "caption"
    #     plt.Table()
    #     plt.plot(x, y)
    #     input_tex = fig.write_input_latex(name, caption=caption, above=False)

    #     # create document for testing input statement
    #     doc = Document()
    #     doc.append(input_tex)
    #     doc.preamble.append(NoEscape(r"\usepackage{graphicx}"))
    #     doc.generate_pdf("Latex/test", clean_tex=False)


if __name__ == "__main__":
    unittest.main()
