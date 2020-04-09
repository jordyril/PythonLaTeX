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


class TestSubTables(unittest.TestCase):
    def test_path(self):
        path = "./Latex/test_path/"
        table = Table(folders_path=path)
        self.assertEqual(table._folders_path, path)
