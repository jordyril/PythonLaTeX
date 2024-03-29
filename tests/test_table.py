from pythonlatex import Table
from pylatex import Document, NoEscape

# from pylatex.base_classes import Arguments
import pandas as pd
import numpy as np

# from pylatex import Document, NoEscape

import unittest

import os
import shutil

try:
    shutil.rmtree("Latex")
except FileNotFoundError:
    pass

# testing DataFrame
df = pd.DataFrame()
x = np.arange(1, 20)
for i in x:
    df[i] = x
# df["x"] = x
# df["y"] = x
df.index.name = "index"


class TestTables(unittest.TestCase):
    def test_path(self):
        path = "./Latex/test_path/"
        table = Table(folders_path=path)
        self.assertEqual(table._folders_path, path)

    def test_inner_folder(self):
        folder = "Inner_test"
        table = Table(inner_folder_name=folder)

        self.assertEqual(table._inner_folder_name, folder)

    def test_outer_folder(self):
        folder = "Outer_test"
        table = Table(outer_folder_name=folder)

        self.assertEqual(table._outer_folder_name, folder)

    def test_position(self):
        position = "h"
        table = Table(position=position)
        self.assertEqual(table.options, position)

    def test_set_tabular(self):
        table = Table()
        table._set_tabular(df)

    def test_save_tabular(self):
        table = Table()
        table._set_tabular(df)
        name = "test"
        table._save_tabular(name)

        # check if graph was saved
        path = table._absolute_inner_path(f"{name}.tex")
        self.assertTrue(os.path.isfile(path))

    def test_add_table(self):
        table = Table()
        table._set_tabular(df)
        name = "test"

        table.add_table(df, name)

        self.assertEqual(
            table.dumps(),
            "\\begin{table}%\n\\centering%\n\\adjustbox{max totalsize={\\textwidth}{0.95\\textheight}}{\\input{Tabulars/test}}%\n\\end{table}",
        )

    def test_caption(self):
        table = Table()
        table._set_tabular(df)
        name = "test"
        caption = "caption"

        table.add_table(df, name, caption=caption)

        self.assertEqual(
            table.dumps(),
            (
                "\\begin{table}%\n\\caption{caption}%\n\\label{tbl:test}%\n\\centering%\n\\adjustbox{max totalsize={\\textwidth}{0.95\\textheight}}{\\input{Tabulars/test}}%\n\\end{table}"
            ),
        )

    def test_reset(self):
        table = Table()
        for i in range(1, 3):
            name = f"test{i}"
            table.add_table(df, name, caption=name)

            # check if correct latex output is produced
            self.assertEqual(
                table.dumps(),
                (
                    f"\\begin{{table}}%\n\\caption{{{name}}}%\n\\label{{tbl:{name}}}%\n\\centering%\n\\adjustbox{{max totalsize={{\\textwidth}}{{0.95\\textheight}}}}{{\\input{{Tabulars/{name}}}}}%\n\\end{{table}}"
                ),
            )
            table.reset()

    def test_texinput(self):
        table = Table()
        name = "test_tex"
        caption = "caption"
        input_tex = table.create_input_latex(df, name, caption=caption, above=False)

        # create document for testing input statement
        doc = Document()
        doc.dumps()
        doc.append(input_tex)
        doc.preamble.append(NoEscape(r"\usepackage{booktabs}"))
        doc.preamble.append(NoEscape(r"\usepackage{zref-user}"))
        doc.preamble.append(NoEscape(r"\usepackage{adjustbox}"))

        doc.generate_pdf(f"Latex/{name}", clean_tex=False)

    def test_adjustbox_default_args(self):
        table = Table()
        name = "test_adjustbox"
        caption = "caption"
        input_tex = table.create_input_latex(
            df, name, caption=caption, above=False, adjustbox=True
        )

        # create document for testing input statement
        doc = Document()
        doc.append(input_tex)
        doc.preamble.append(NoEscape(r"\usepackage{booktabs}"))
        doc.preamble.append(NoEscape(r"\usepackage{zref-user}"))
        doc.preamble.append(NoEscape(r"\usepackage{adjustbox}"))
        # doc.generate_tex(f"Latex/{name}")
        doc.generate_pdf(f"Latex/{name}", clean_tex=False)

    def test_adjustbox_user_args(self):
        table = Table()
        name = "test_adjustbox2"
        caption = "caption"
        input_tex = table.create_input_latex(
            df,
            name,
            caption=caption,
            above=False,
            adjustbox=True,
            adjustbox_arguments=NoEscape(r"max totalsize={\textwidth}{0.2\textheight}"),
        )

        # create document for testing input statement
        doc = Document()
        doc.append(input_tex)
        doc.preamble.append(NoEscape(r"\usepackage{booktabs}"))
        doc.preamble.append(NoEscape(r"\usepackage{zref-user}"))
        doc.preamble.append(NoEscape(r"\usepackage{adjustbox}"))
        # doc.generate_tex(f"Latex/{name}")
        doc.generate_pdf(f"Latex/{name}", clean_tex=False)

    def test_resizebox_default_args(self):
        table = Table()
        name = "test_resizebox"
        caption = "caption"
        input_tex = table.create_input_latex(
            df,
            name,
            caption=caption,
            above=False,
            resizebox=True,
            adjustbox=False,
        )

        # create document for testing input statement
        doc = Document()
        doc.append(input_tex)
        doc.preamble.append(NoEscape(r"\usepackage{booktabs}"))
        doc.preamble.append(NoEscape(r"\usepackage{zref-user}"))
        doc.preamble.append(NoEscape(r"\usepackage{graphics}"))
        # doc.generate_tex(f"Latex/{name}")
        doc.generate_pdf(f"Latex/{name}", clean_tex=False)

    def test_resizebox_user_args(self):
        table = Table()
        name = "test_resizebox"
        caption = "caption"
        input_tex = table.create_input_latex(
            df,
            name,
            caption=caption,
            above=False,
            resizebox=True,
            resizebox_arguments=(NoEscape("\columnwidth"), NoEscape("!")),
            adjustbox=False,
        )

        # create document for testing input statement
        doc = Document()
        doc.append(input_tex)
        doc.preamble.append(NoEscape(r"\usepackage{booktabs}"))
        doc.preamble.append(NoEscape(r"\usepackage{zref-user}"))
        doc.preamble.append(NoEscape(r"\usepackage{graphics}"))
        # doc.generate_tex(f"Latex/{name}")
        doc.generate_pdf(f"Latex/{name}", clean_tex=False)

    def resizebox_adjustbox_error(self):
        table = Table()
        name = "test_resizebox_adjsutbox_error"

        _ = table.create_input_latex(
            df,
            name,
            resizebox=True,
            adjustbox=True,
        )
        return None

    def test_resizebox_adjustbox_error(self):
        with self.assertRaises(Exception) as context:
            self.resizebox_adjustbox_error()
        self.assertTrue(
            "Cannot have both resizebox and adjustbox" in str(context.exception)
        )


if __name__ == "__main__":
    unittest.main()
