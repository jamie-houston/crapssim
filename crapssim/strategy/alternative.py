from enum import Enum


class AlternativeStrategy(Enum):
    pass


class ChangeFieldBet(AlternativeStrategy):
    """
    Don't bet the field
    """
    Never = 0,
    Always = 1,
    OnComeOut = 2,
    OnActivePoint = 3,
    # on comeout or active point?


class HedgeBet(AlternativeStrategy):
    """
    Hedge bets on table
    HardNumbers : whenever a DP/DC is on a hard number, bet it
    DontCrapOut : When a bet can lose with craps, bet it (11 on DP/DC, 2,3,12 on PassLine/Come)
    """
    HardNumbers = 0,
    DontCrapOut = 1,


class LevelBetting(AlternativeStrategy):
    """
    Change amount of bet
    Same Unit - same unit every bet
    Double Unit - double units
    Increment Unit - Go up by a unit
    On Profit Loss - Only when current balance is below starting balance
    On Crap Out - Only when current balance is below starting balance
    """
    SameUnit = 0,
    DoubleUnit = 1,
    IncrementUnit = 2
    OnProfileLoss = 3,
    OnCrapOut = 4
