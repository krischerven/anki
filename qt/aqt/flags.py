# Copyright: Ankitects Pty Ltd and contributors
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
from __future__ import annotations

from dataclasses import dataclass
from typing import cast

import aqt
import aqt.main
from anki.collection import SearchNode
from aqt import colors, gui_hooks
from aqt.theme import ColoredIcon
from aqt.utils import tr


@dataclass
class Flag:
    """A container class for flag related data.

    index -- The integer by which the flag is represented internally (1-7).
    label -- The text by which the flag is described in the GUI.
    icon -- The icon by which the flag is represented in the GUI.
    search_node -- The node to build a search string for finding cards with the flag.
    action -- The name of the action to assign the flag in the browser form.
    """

    index: int
    label: str
    icon: ColoredIcon
    search_node: SearchNode
    action: str


class FlagManager:
    def __init__(self, mw: aqt.main.AnkiQt) -> None:
        self.mw = mw
        self._flags: list[Flag] = []

    def all(self) -> list[Flag]:
        """Return a list of all flags."""
        if not self._flags:
            self._load_flags()
        return self._flags

    def get_flag(self, flag_index: int) -> Flag:
        if not 1 <= flag_index <= len(self.all()):
            raise Exception(f"Flag index out of range (1-{len(self.all())}).")
        return self.all()[flag_index - 1]

    def rename_flag(self, flag_index: int, new_name: str) -> None:
        if new_name in ("", self.get_flag(flag_index).label):
            return
        labels = self.mw.col.get_config("flagLabels", {})
        labels[str(flag_index)] = self.get_flag(flag_index).label = new_name
        self.mw.col.set_config("flagLabels", labels)
        gui_hooks.flag_label_did_change()

    def restore_default_flag_name(self, flag_index: int) -> None:
        labels = self.mw.col.get_config("flagLabels", {})
        if str(flag_index) not in labels:
            return
        del labels[str(flag_index)]
        self.mw.col.set_config("flagLabels", labels)
        self.require_refresh()
        gui_hooks.flag_label_did_change()

    def require_refresh(self) -> None:
        "Discard cached labels."
        self._flags = []

    def _load_flags(self) -> None:
        labels = cast(dict[str, str], self.mw.col.get_config("flagLabels", {}))
        icon = ColoredIcon(path="icons:flag-variant.svg", color=colors.FG_DISABLED)

        self._flags = [
            Flag(
                1,
                labels["1"] if "1" in labels else tr.actions_flag_red(),
                icon.with_color(colors.FLAG_1),
                SearchNode(flag=SearchNode.FLAG_RED),
                "actionRed_Flag",
            ),
            Flag(
                2,
                labels["2"] if "2" in labels else tr.actions_flag_orange(),
                icon.with_color(colors.FLAG_2),
                SearchNode(flag=SearchNode.FLAG_ORANGE),
                "actionOrange_Flag",
            ),
            Flag(
                3,
                labels["3"] if "3" in labels else tr.actions_flag_green(),
                icon.with_color(colors.FLAG_3),
                SearchNode(flag=SearchNode.FLAG_GREEN),
                "actionGreen_Flag",
            ),
            Flag(
                4,
                labels["4"] if "4" in labels else tr.actions_flag_blue(),
                icon.with_color(colors.FLAG_4),
                SearchNode(flag=SearchNode.FLAG_BLUE),
                "actionBlue_Flag",
            ),
            Flag(
                5,
                labels["5"] if "5" in labels else tr.actions_flag_pink(),
                icon.with_color(colors.FLAG_5),
                SearchNode(flag=SearchNode.FLAG_PINK),
                "actionPink_Flag",
            ),
            Flag(
                6,
                labels["6"] if "6" in labels else tr.actions_flag_turquoise(),
                icon.with_color(colors.FLAG_6),
                SearchNode(flag=SearchNode.FLAG_TURQUOISE),
                "actionTurquoise_Flag",
            ),
            Flag(
                7,
                labels["7"] if "7" in labels else tr.actions_flag_purple(),
                icon.with_color(colors.FLAG_7),
                SearchNode(flag=SearchNode.FLAG_PURPLE),
                "actionPurple_Flag",
            ),
        ]
