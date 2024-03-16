from enum import Enum


class AlternativeStrategy(Enum):
    pass


class ChangeFieldBet(AlternativeStrategy):
    """
    Don't bet the field
    """
    Never = False,
    Always = True,
    # on comeout or active point?


class HedgeBet(AlternativeStrategy):
    """
    Hedge bets on table
    HardNumbers : whenever a DP/DC is on a hard number, bet it
    DontCrapOut : When a bet can lose with craps, bet it (11 on DP/DC, 2,3,12 on PassLine/Come)
    """
    HardNumbers = 0,
    DontCrapOut = 1,
