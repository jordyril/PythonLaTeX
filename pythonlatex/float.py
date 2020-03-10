"""
"""
from pylatex import Command, NoEscape, Package
from pylatex.base_classes import Float


class FloatAdditions(Float):
    def __init__(self):
        self._label = ""

    def add_caption_description(self, caption, above=True, description=None):
        """Add a caption to the float.
        Args
        ----
        caption: str
            The text of the caption.
        above: bool
            Position of caption
        description: str
            The text for an accompanying description bellow caption
        """
        if above:
            if description:
                self.insert(0, Command('caption*'), description)
            self.insert(0, Command("caption", caption))

        else:
            self.append(Command("caption", caption))
            if description:
                self.append(0, Command('caption*'), description)

    def add_label(self, label, above=True):
        self.packages.add(Package("zref-user"))
        if above:
            self.insert(0, Command(
                "zlabel", NoEscape(f"{self._label}:{label}")))
        else:
            self.append(Command("zlabel", NoEscape(f"{self._label}:{label}")))

    def add_caption_description_label(self, caption, label, above=True, description=None):
        if above:
            # note that we do label first here, so in final label is after caption
            self.add_label(NoEscape(label), above)
            self.add_caption_description(caption, above, description)
        else:
            self.add_caption_description(caption, above, description)
            self.add_label(NoEscape(label), above)
