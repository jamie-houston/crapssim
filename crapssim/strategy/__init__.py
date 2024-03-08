__all__ = ["table", "player", "dice", "strategy", "bet"]

from crapssim.table import Table
from crapssim.player import Player
from crapssim.dice import Dice

# Don't require ic import in any module
from icecream import install
install()