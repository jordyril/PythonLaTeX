from pythonlatex import Table
from pylatex import Document, NoEscape
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
x = np.arange(1, 5)
df["x"] = x
df["y"] = x
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
            "\\begin{table}%\n\\centering%\n\\input{Tabulars/test}%\n\\end{table}",
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
                "\\begin{table}%\n\\caption{caption}%\n\\zlabel{tbl:test}%\n\\"
                "centering%\n\\input{Tabulars/test}%\n\\end{table}"
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
                    f"\\begin{{table}}%\n\\caption{{{name}}}%\n\\zlabel{{tbl:{name}}}%\n\\"
                    f"centering%\n\\input{{Tabulars/{name}}}%\n\\end{{table}}"
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
        doc.append(input_tex)
        doc.preamble.append(NoEscape(r"\usepackage{booktabs}"))
        doc.preamble.append(NoEscape(r"\usepackage{zref-user}"))
        doc.generate_pdf("Latex/test", clean_tex=False)


if __name__ == "__main__":
    unittest.main()
