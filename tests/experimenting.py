import numpy as np
from pylatex import Table as TableOriginal
from pylatex import NoEscape, Tabular, Command
from pylatex.base_classes import Options, Arguments
from pythonlatex import Table
from pythonlatex.table import StandAloneTabular
import pandas as pd

df = pd.DataFrame()
x = np.arange(1, 5)
df["x"] = x
df["y"] = x
df.index.name = "index"

to_latex = df.to_latex()
# print(to_latex)

tabular = Tabular("lll")
tabular.add_row((1, 2, 3))
tabular.add_row((1, 2, 3))

tab = Table()
tab._set_tabular(df)
tab._save_tabular("test")


tab.tabular

input_tabular = NoEscape(StandAloneTabular(filename="test").dumps())

Command("adjustbox")

tab.append(StandAloneTabular(filename="test"))
tab.dumps()

tab.dumps()

tab.data

print(tab.dumps())


# ## adjustbox feature
#         input_tex.write(
#             "\\adjustbox{max totalsize={"
#             + adjustbox[0]
#             + "}{"
#             + adjustbox[1]
#             + "}}{ \n"
#         )
test = Command(
    command="adjustbox",
    arguments=Arguments(NoEscape(r"max totalsize={\textwidth}{0.95\textheight}")),
    extra_arguments=input_tabular,
)

"max totalsize={\textwidth}{0.95\textheight}"
print(test.dumps())
