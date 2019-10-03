import numpy as np
import matplotlib.pyplot as plt
from pythonlatex import Figure
from pylatex import Document, NoEscape

import unittest
import os
import shutil

a = 0.0
b = 2.0
n = 50

x = np.array(range(1, n + 1))
y = a + b * x

try:
    shutil.rmtree("Latex")
except FileNotFoundError:
    pass


class TestFigures(unittest.TestCase):
    def test_path(self):
        path = "./Latex/test_path/"
        fig = Figure(folders_path=path)
        self.assertEqual(fig._folders_path, path)

    def test_inner_folder(self):
        folder = "Inner_test"
        fig = Figure(inner_folder_name=folder)

        self.assertEqual(fig._inner_folder_name, folder)

    def test_outer_folder(self):
        folder = "Outer_test"
        fig = Figure(outer_folder_name=folder)

        self.assertEqual(fig._outer_folder_name, folder)

    def test_position(self):
        position = "h"
        fig = Figure(position=position)
        self.assertEqual(fig.options, position)

    def test_save_plot(self):
        fig = Figure()
        name = "test"
        plt.figure()
        plt.plot(x, y)
        fig._save_plot(name)

        # check if graph was saved
        path = fig._absolute_inner_path(f"{name}.jpg")
        self.assertTrue(os.path.isfile(path))

    def test_add_plot(self):
        fig = Figure()
        name = "test"
        plt.figure()
        plt.plot(x, y)
        fig.add_plot(name)

        # check if correct latex output is produced
        self.assertEqual(
            fig.dumps(),
            (
                "\\begin{figure}%\n\\centering%\n\\includegraphics[width=0.8"
                + "\\textwidth]{Graphs/test.jpg}%\n\\end{figure}"
            ),
        )
        plt.close()

    def test_reset(self):
        fig = Figure()
        # figure 1
        for i in range(1, 3):
            name = f"test{i}"
            plt.figure()
            plt.plot(x, y, label=i)
            fig.add_plot(name)

            # check if correct latex output is produced
            self.assertEqual(
                fig.dumps(),
                (
                    f"\\begin{{figure}}%\n\\centering%\n\\includegraphics[width=0.8\\textwidth]"
                    + f"{{Graphs/test{i}.jpg}}%\n\\end{{figure}}"
                ),
            )
            fig.reset(show=False, close=True)

    def test_texinput(self):
        fig = Figure()
        name = "test_tex"
        caption = "caption"
        plt.figure()
        plt.plot(x, y)
        input_tex = fig.create_input_latex(name, caption=caption, above=False)

        # create document for testing input statement
        doc = Document()
        doc.append(input_tex)
        doc.preamble.append(NoEscape(r"\usepackage{graphicx}"))
        doc.preamble.append(NoEscape(r"\usepackage{zref-user}"))
        doc.generate_pdf("Latex/test_tex", clean_tex=False)

    def test_label(self):
        fig = Figure()
        name = "test_label"
        caption = "caption"
        label = "label"
        plt.figure()
        plt.plot(x, y)

        input_tex = fig.create_input_latex(
            name, caption=caption, above=True, label=label
        )

        # create document for testing input statement
        doc = Document()
        doc.append(input_tex)
        doc.preamble.append(NoEscape(r"\usepackage{graphicx}"))
        doc.preamble.append(NoEscape(r"\usepackage{zref-user}"))
        doc.generate_pdf("Latex/test_label", clean_tex=False)


if __name__ == "__main__":
    unittest.main()
