"""
"""
from pylatex import Command, NoEscape, Package
from pylatex.base_classes import Float


class FloatAdditions(Float):
    def __init__(self):
        self._label = ""

    def add_caption(self, caption, above=True):
        """Add a caption to the float.
        Args
        ----
        caption: str
            The text of the caption.
        above: bool
            Position of caption
        """
        if above:
            self.insert(0, Command("caption", caption))

        else:
            self.append(Command("caption", caption))

    def add_label(self, label, above=True):
        self.packages.add(Package("zref-user"))
        if above:
            self.insert(0, Command("zlabel", NoEscape(f"{self._label}:{label}")))
        else:
            self.append(Command("zlabel", NoEscape(f"{self._label}:{label}")))

    def add_caption_label(self, caption, label, above=True):
        if above:
            # note that we do label first here, so in final label is after caption
            self.add_label(NoEscape(label), above)
            self.add_caption(caption, above)
        else:
            self.add_caption(caption, above)
            self.add_label(NoEscape(label), above)
