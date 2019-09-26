from pythonlatex import LatexFigure
import unittest


class TestInit(unittest.TestCase):
    def test_path(self):
        path = "./test"
        fig = LatexFigure(folder_path=path, create_folder=False)
        self.assertEqual(fig._folder_path, path)

    def test_folder(self):
        folder = "test_folder"
        fig = LatexFigure(folder_name=folder, create_folder=False)

        self.assertEqual(fig._folder_name, folder)

    def test_position(self):
        position = "h"
        fig = LatexFigure(position=position, create_folder=False)
        self.assertEqual(fig.options, position)


if __name__ == "__main__":
    unittest.main()
