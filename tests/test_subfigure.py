import numpy as np
import matplotlib.pyplot as plt
from pythonlatex import Figure, SubFigure
from pylatex import Document, NoEscape

import unittest
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


class TestSubFigure(unittest.TestCase):
    def test_two(self):
        doc = Document()
        fig = Figure()
        with doc.create(Figure()) as fig:
            with fig.create(SubFigure(width=NoEscape(r"0.48\textwidth"))) as left:
                name = "left"
                plt.figure()
                plt.plot(x, y, label="l")
                plt.legend()
                left.add_plot(name, caption=name)
                plt.close()

            with fig.create(SubFigure(width=NoEscape(r"0.48\textwidth"))) as right:
                name = "right"
                plt.figure()
                plt.plot(x, y, label="r")
                plt.legend()
                right.add_plot(name, caption=name)
                plt.close()

            fig.add_caption_label("full", "full", above=False)

            self.assertEqual(
                fig.dumps(),
                (
                    "\\begin{figure}%\n\\begin{subfigure}{0.48\\textwidth}%"
                    + "\n\\caption{left}%\n\\zlabel{fig:left}%\n\\includegraphics[width=\\linewidth]"
                    + "{Graphs/left.jpg}%\n\\end{subfigure}%\n\\begin{subfigure}{0.48\\textwidth}%"
                    + "\n\\caption{right}%\n\\zlabel{fig:right}%\n\\includegraphics[width="
                    + "\\linewidth]{Graphs/right.jpg}%\n\\end{subfigure}%\n\\caption{full}%\n"
                    + "\\zlabel{fig:full}%\n\\end{figure}"
                ),
            )
        doc.generate_tex("Latex/twosubfigures")

    def test_three(self):
        doc = Document()
        with doc.create(Figure()) as fig:
            with fig.create(SubFigure(width=NoEscape(r"0.48\textwidth"))) as left:
                name = "left"
                plt.figure()
                plt.plot(x, y, label="l")
                plt.legend()
                left.add_plot(name, caption=name)
                plt.close()

            with fig.create(SubFigure(width=NoEscape(r"0.48\textwidth"))) as right:
                name = "right"
                plt.figure()
                plt.plot(x, y, label="r")
                plt.legend()
                right.add_plot(name, caption=name)
                plt.close()

            fig.append("\n")

            with fig.create(SubFigure(width=NoEscape(r"0.48\textwidth"))) as left2:
                name = "left2"
                plt.figure()
                plt.plot(x, y, label="l2")
                plt.legend()
                left2.add_plot(name, caption=name)
                plt.close()

            fig.add_caption("full")
        doc.generate_tex("Latex/threesubfigures")

    def test_four(self):
        doc = Document()
        with doc.create(Figure()) as fig:

            with fig.create(SubFigure(width=NoEscape(r"0.48\textwidth"))) as left:
                name = "left"
                plt.figure()
                plt.plot(x, y, label="l")
                plt.legend()
                left.add_plot(name, caption=name)
                plt.close()

            with fig.create(SubFigure(width=NoEscape(r"0.48\textwidth"))) as right:
                name = "right"
                plt.figure()
                plt.plot(x, y, label="r")
                plt.legend()
                right.add_plot(name, caption=name)
                plt.close()

            fig.append("\n")

            with fig.create(SubFigure(width=NoEscape(r"0.48\textwidth"))) as left2:
                name = "left2"
                plt.figure()
                plt.plot(x, y, label="l2")
                plt.legend()
                left2.add_plot(name, caption=name)
                plt.close()

            with fig.create(SubFigure(width=NoEscape(r"0.48\textwidth"))) as right2:
                name = "right2"
                plt.figure()
                plt.plot(x, y, label="r2")
                plt.legend()
                right2.add_plot(name, caption=name)
                plt.close()

            fig.add_caption("full")
        doc.generate_tex("Latex/foursubfigures")

    def test_latexinput(self):
        doc = Document()
        with doc.create(Figure()) as fig:

            with fig.create(SubFigure(width=NoEscape(r"0.48\textwidth"))) as left:
                name = "left"
                plt.figure()
                plt.plot(x, y, label="l")
                plt.legend()
                left.add_plot(name, caption=name)
                plt.close()

            with fig.create(SubFigure(width=NoEscape(r"0.48\textwidth"))) as right:
                name = "right"
                plt.figure()
                plt.plot(x, y, label="r")
                plt.legend()
                right.add_plot(name, caption=name)
                plt.close()

            fig.append("\n")

            with fig.create(SubFigure(width=NoEscape(r"0.48\textwidth"))) as left2:
                name = "left2"
                plt.figure()
                plt.plot(x, y, label="l2")
                plt.legend()
                left2.add_plot(name, caption=name)
                plt.close()

            with fig.create(SubFigure(width=NoEscape(r"0.48\textwidth"))) as right2:
                name = "right2"
                plt.figure()
                plt.plot(x, y, label="r2")
                plt.legend()
                right2.add_plot(name, caption=name)
                plt.close()

            # fig.add_caption_label("full", "full")
            input_tex = fig.create_input_latex(
                "test", add_plot=False, caption="full", label="full", above=False
            )

        # create document for testing input statement
        doc = Document()
        doc.preamble.append(NoEscape(r"\usepackage{graphicx}"))
        doc.preamble.append(NoEscape(r"\usepackage{zref-user}"))
        doc.preamble.append(NoEscape(r"\usepackage{subcaption}"))
        doc.append(input_tex)
        doc.generate_pdf("Latex/test", clean_tex=False)


if __name__ == "__main__":
    unittest.main()
