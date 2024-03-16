from crapssim.bet import PassLine, Odds, Come
from crapssim.bet import DontPass, LayOdds
from crapssim.bet import Place, Place4, Place5, Place6, Place8, Place9, Place10, SingleRoll
from crapssim.bet import Field, Horn, Hard

"""
Various betting strategies that are based on conditions of the CrapsTable.
Each strategy must take a table and a player_object, and implicitly 
uses the methods from the player object.
"""

"""
Custom Strategies
"""

"""
Fundamental Strategies
"""

def passline(player, table, unit=5, strat_info=None):
    # Pass line bet
    if table.point.is_off() and not player.has_bet("PassLine"):
        player.bet(PassLine(unit))

def dontpass(player, table, unit=5, odds=0):
    # Don't pass bet
    if table.point.is_off() and not player.has_bet("DontPass"):
        player.bet(DontPass(unit))
