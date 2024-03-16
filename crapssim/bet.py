import decimal
from dataclasses import dataclass
from enum import Enum

from crapssim.dice import Dice

"""
Supported Bet Types
- Multi-Roll
    - Pass/Don't Pass
        - Odds
    - Come/Don't Come
        - Odds
    - Place
- Single-Roll
    - Field
    - Hard (2,4,6,8,10,12) - Note - I'm cheating with 2 and 12 instead of horn bets
    - Horn


- TODO:
    - Lay
    - Win
    - Move Horn bets from hard and lay individual numbers (2,3,11,12)
    - CE
    - Seven
    - Any Craps
"""


class Bet():
    """
    A generic bet for the craps table

    Parameters
    ----------
    bet_amount : float
        Wagered amount for the bet

    Attributes
    ----------
    name : string
        Name for the bet
    subname : string
        Subname, usually denotes number for a come/don't come bet
    winning_numbers : list
        Numbers to roll for this bet to win
    losing_numbers : list
        Numbers to roll that cause this bet to lose
    payoutratio : float
        Ratio that bet pays out on a win


    """

    name = None
    subname = ""
    winning_numbers = []
    losing_numbers = []
    payoutratio = float(1)
    remove_on_win = True

    def __init__(self, bet_amount):
        self.bet_amount = round(bet_amount, 2)

    def is_bet_type(self, bet_type):
        return self.name == bet_type.__name__

    def _update_bet(self, table_object, dice_object: Dice):
        result = BetResult(status=BetStatus.PUSH)

        if dice_object.total in self.winning_numbers:
            result.status = BetStatus.WIN
            result.win_amount = self.payoutratio * self.bet_amount
        elif len(self.losing_numbers) == 0 or dice_object.total in self.losing_numbers:
            result.status = BetStatus.LOSE

        return result

    def __str__(self):
        return self.name + " " + self.subname

    def __repr__(self) -> str:
        return self.name + " " + self.subname


"""
Passline and Come bets
"""


class PassLine(Bet):
    # TODO: make this require that table_object.point = "Off",
    # probably better in the player module
    def __init__(self, bet_amount):
        self.name = "PassLine"
        self.winning_numbers = [7, 11]
        self.losing_numbers = [2, 3, 12]
        self.prepoint = True
        super().__init__(bet_amount)

    def _update_bet(self, table_object, dice_object):
        result = BetResult(status=BetStatus.PUSH)

        if dice_object.total in self.winning_numbers:
            result.status = BetStatus.WIN
            result.win_amount = self.payoutratio * self.bet_amount
        elif dice_object.total in self.losing_numbers:
            result.status = BetStatus.LOSE
        elif self.prepoint:
            self.winning_numbers = [dice_object.total]
            self.losing_numbers = [7]
            self.prepoint = False

        return result


class Come(PassLine):
    def __init__(self, bet_amount):
        super().__init__(bet_amount)
        self.name = "Come"

    def _update_bet(self, table_object, dice_object):
        result = super()._update_bet(table_object, dice_object)
        if not self.prepoint and self.subname == "":
            self.subname = "".join(str(e) for e in self.winning_numbers)
        return result


"""
Passline/Come bet odds
"""


class Odds(Bet):
    def __init__(self, bet_amount, bet_object):
        super().__init__(bet_amount)
        self.name = "Odds"
        self.subname = "".join(str(e) for e in bet_object.winning_numbers)
        self.winning_numbers = bet_object.winning_numbers
        self.losing_numbers = bet_object.losing_numbers

        # TODO: Payout is opposite for dont pass/dont come (self.winning_numbers == [7])
        if self.winning_numbers == [4] or self.winning_numbers == [10]:
            self.payoutratio = 2 / 1
        elif self.winning_numbers == [5] or self.winning_numbers == [9]:
            self.payoutratio = 3 / 2
        elif self.winning_numbers == [6] or self.winning_numbers == [8]:
            self.payoutratio = 6 / 5
        elif self.winning_numbers == [7]:
            if self.losing_numbers == [4] or self.losing_numbers == [10]:
                self.payoutratio = 5 / 6
            elif self.losing_numbers == [5] or self.losing_numbers == [9]:
                self.payoutratio = 2 / 3
            elif self.losing_numbers == [6] or self.losing_numbers == [8]:
                self.payoutratio = 5 / 6


"""
Place Bets on 4,5,6,8,9,10
"""


class Place(Bet):
    remove_on_win = False

    def _update_bet(self, table_object, dice_object):
        # place bets are inactive when point is "Off"
        if table_object.point.is_on():
            return super()._update_bet(table_object, dice_object)
        else:
            return BetResult()


class Place4(Place):
    def __init__(self, bet_amount):
        self.name = "Place4"
        self.winning_numbers = [4]
        self.losing_numbers = [7]
        self.payoutratio = 9 / 5
        super().__init__(bet_amount)


class Place5(Place):
    def __init__(self, bet_amount):
        self.name = "Place5"
        self.winning_numbers = [5]
        self.losing_numbers = [7]
        self.payoutratio = 7 / 5
        super().__init__(bet_amount)


class Place6(Place):
    def __init__(self, bet_amount):
        self.name = "Place6"
        self.winning_numbers = [6]
        self.losing_numbers = [7]
        self.payoutratio = 7 / 6
        super().__init__(bet_amount)


class Place8(Place):
    def __init__(self, bet_amount):
        self.name = "Place8"
        self.winning_numbers = [8]
        self.losing_numbers = [7]
        self.payoutratio = 7 / 6
        super().__init__(bet_amount)


class Place9(Place):
    def __init__(self, bet_amount):
        self.name = "Place9"
        self.winning_numbers = [9]
        self.losing_numbers = [7]
        self.payoutratio = 7 / 5
        super().__init__(bet_amount)


class Place10(Place):
    def __init__(self, bet_amount):
        self.name = "Place10"
        self.winning_numbers = [10]
        self.losing_numbers = [7]
        self.payoutratio = 9 / 5
        super().__init__(bet_amount)


"""
Field bet
"""


class Field(Bet):
    """
    Parameters
    ----------
    double : list
        Set of numbers that pay double on the field bet (default = [2,12])
    triple : list
        Set of numbers that pay triple on the field bet (default = [])
    """

    def __init__(self, bet_amount, double=[2, 12], triple=[]):
        self.name = "Field"
        self.double_winning_numbers = double
        self.triple_winning_numbers = triple
        self.winning_numbers = [2, 3, 4, 9, 10, 11, 12]
        self.losing_numbers = [5, 6, 7, 8]
        super().__init__(bet_amount)

    def _update_bet(self, table_object, dice_object):
        result = BetResult(status=BetStatus.PUSH)

        if dice_object.total in self.triple_winning_numbers:
            result.status = BetStatus.WIN
            result.win_amount = 3 * self.bet_amount
        elif dice_object.total in self.double_winning_numbers:
            result.status = BetStatus.WIN
            result.win_amount = 2 * self.bet_amount
        elif dice_object.total in self.winning_numbers:
            result.status = BetStatus.WIN
            result.win_amount = 1 * self.bet_amount
        elif dice_object.total in self.losing_numbers:
            result.status = BetStatus.LOSE

        return result


"""
Don't pass and Don't come bets
"""


class DontPass(Bet):
    # TODO: make this require that table_object.point = "Off",
    #  probably better in the player module
    def __init__(self, bet_amount):
        self.name = "DontPass"
        self.winning_numbers = [2, 3]
        self.losing_numbers = [7, 11]
        self.push_numbers = [12]
        self.prepoint = True
        super().__init__(bet_amount)

    def _update_bet(self, table_object, dice_object):
        result = BetResult(status=BetStatus.PUSH)

        if dice_object.total in self.winning_numbers:
            result.status = BetStatus.WIN
            result.win_amount = self.payoutratio * self.bet_amount
        elif dice_object.total in self.losing_numbers:
            result.status = BetStatus.LOSE
        elif dice_object.total in self.push_numbers:
            # status = "push"
            pass
        elif self.prepoint:
            self.winning_numbers = [7]
            self.losing_numbers = [dice_object.total]
            self.push_numbers = []
            self.prepoint = False
            self.subname = "".join(str(e) for e in self.losing_numbers)

        return result


class DontCome(DontPass):
    def __init__(self, bet_amount):
        super().__init__(bet_amount)
        self.name = "DontCome"


"""
Don't pass/Don't come lay odds
"""


class LayOdds(Bet):
    def __init__(self, bet_amount, bet_object):
        super().__init__(bet_amount)
        self.name = "LayOdds"
        self.subname = "".join(str(e) for e in bet_object.losing_numbers)
        self.winning_numbers = bet_object.winning_numbers
        self.losing_numbers = bet_object.losing_numbers

        if self.losing_numbers == [4] or self.losing_numbers == [10]:
            self.payoutratio = 1 / 2
        elif self.losing_numbers == [5] or self.losing_numbers == [9]:
            self.payoutratio = 2 / 3
        elif self.losing_numbers == [6] or self.losing_numbers == [8]:
            self.payoutratio = 5 / 6


class Horn(Bet):
    def __init__(self, bet_amount):
        super().__init__(bet_amount)
        self.name = "Horn"
        self.winning_numbers = [2, 3, 11, 12]
        self.subname = "".join(str(e) for e in self.winning_numbers)
        self.losing_numbers = [4, 5, 6, 7, 8, 9, 10]

    def _update_bet(self, table_object, dice_object):
        result = BetResult(status=BetStatus.LOSE)

        if dice_object.total in [2, 12]:
            result.status = BetStatus.WIN
            result.win_amount = (30 / 4) * self.bet_amount
        elif dice_object.total in [3, 11]:
            result.status = BetStatus.WIN
            result.win_amount = (15 / 4) * self.bet_amount

        return result


class Hard(Bet):
    def __init__(self, bet_amount, hard_number):
        super().__init__(bet_amount)
        self.name = "Hard"
        self.subname = str(hard_number)
        self.winning_numbers = [hard_number]
        self.losing_numbers = [7]
        if any(set(self.winning_numbers).intersection([4, 10])):
            self.payoutratio = 9
        elif any(set(self.winning_numbers).intersection([6, 8])):
            self.payoutratio = 7
        else:
            raise Exception("Invalid bet")

    def _update_bet(self, table_object, dice_object):
        result = BetResult(status=BetStatus.PUSH)

        if dice_object.total in self.winning_numbers:
            if dice_object.result[0] == dice_object.result[1]:
                result.status = BetStatus.WIN
                result.win_amount = self.payoutratio * self.bet_amount
            else:
                result.status = BetStatus.LOSE
        else:
            return super()._update_bet(table_object, dice_object)

        return result


class SingleRoll(Bet):
    def __init__(self, bet_amount, winning_number):
        super().__init__(bet_amount)
        self.name = str(winning_number)
        self.subname = "Single Roll"
        self.winning_numbers = [winning_number]
        self.losing_numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        self.losing_numbers.remove(winning_number)
        if any(set(self.winning_numbers).intersection([2, 12])):
            self.payoutratio = 30
        elif any(set(self.winning_numbers).intersection([3, 11])):
            self.payoutratio = 15
        else:
            raise Exception("Invalid bet")

    def _update_bet(self, table_object, dice_object):
        result = BetResult(status=BetStatus.LOSE)
        if dice_object.total in self.winning_numbers:
            result.status = BetStatus.WIN
            result.win_amount = self.payoutratio * self.bet_amount

        return result


class BetStatus(Enum):
    WIN = "win",
    LOSE = "lose",
    PUSH = "push"


@dataclass
class BetResult(Bet):
    status: BetStatus = BetStatus.PUSH
    win_amount: decimal = 0
