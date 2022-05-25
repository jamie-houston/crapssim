import typing
from abc import ABC, abstractmethod

if typing.TYPE_CHECKING:
    from crapssim.table import Table
    from crapssim import Player, Table


class Bet(ABC):
    """
    A generic bet for the craps table

    Parameters
    ----------
    bet_amount : typing.SupportsFloat
        Wagered amount for the bet

    Attributes
    ----------
    bet_amount: float
        Wagered amount for the bet
    """

    def __init__(self, bet_amount: typing.SupportsFloat):
        self.bet_amount: float = float(bet_amount)

    @abstractmethod
    def get_payout_ratio(self, table: "Table") -> float:
        pass

    @property
    def name(self) -> str:
        return self.__class__.__name__

    def is_removable(self, player: "Player") -> bool:
        return True

    def allowed(self, player: "Player") -> bool:
        """
        Checks whether the bet is allowed to be placed on the given table.

        Parameters
        ----------
        player

        Returns
        -------
        bool
            True if the bet is allowed, otherwise false.
        """
        return True

    @abstractmethod
    def get_status(self, table: "Table") -> str | None:
        pass

    def get_win_amount(self, table: "Table") -> float:
        if self.get_status(table) == "win":
            return self.get_payout_ratio(table) * self.bet_amount
        return 0.0

    def get_return_amount(self, table: "Table") -> float:
        status = self.get_status(table)
        if status == "win":
            return self.get_win_amount(table) + self.bet_amount
        if status is None and self.should_remove(table) is True:
            return self.bet_amount
        else:
            return 0

    def should_remove(self, table: "Table") -> bool:
        if self.get_status(table) is not None:
            return True
        return False

    def update(self, table: "Table") -> None:
        """
        Returns whether the bets status is win, lose or None and if win the amount won.

        Returns
        -------
        tuple[str | None, float]
            The status of the bet and the amount of the winnings.
        """
        pass

    def already_placed(self, player: "Player") -> bool:
        return player.has_bets_by_type(type(self))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Bet):
            return isinstance(other, type(self)) and other.bet_amount == self.bet_amount
        else:
            raise NotImplementedError

    @abstractmethod
    def __hash__(self) -> int:
        pass

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(bet_amount={self.bet_amount})'


class WinningLosingNumbersBet(Bet, ABC):
    @abstractmethod
    def get_winning_numbers(self, table: "Table") -> list[int]:
        pass

    @abstractmethod
    def get_losing_numbers(self, table: "Table") -> list[int]:
        pass

    def get_status(self, table: "Table") -> str | None:
        if table.dice.total in self.get_winning_numbers(table):
            return "win"
        elif table.dice.total in self.get_losing_numbers(table):
            return "lose"
        return None


class StaticWinningLosingNumbersBet(WinningLosingNumbersBet):
    @property
    @abstractmethod
    def winning_numbers(self) -> list[int]:
        pass

    @property
    @abstractmethod
    def losing_numbers(self) -> list[int]:
        pass

    def get_winning_numbers(self, table: "Table") -> list[int]:
        return self.winning_numbers

    def get_losing_numbers(self, table: "Table") -> list[int]:
        return self.losing_numbers

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Bet):
            return isinstance(other, type(self)) and \
                   self.winning_numbers == other.winning_numbers and \
                   self.losing_numbers == other.losing_numbers and \
                   self.bet_amount == other.bet_amount
        else:
            raise NotImplementedError


"""
Passline and Come bets
"""


class BaseOdds(StaticWinningLosingNumbersBet, ABC):
    @property
    @abstractmethod
    def base_bet_types(self) -> tuple[typing.Type["AllowsOdds"], ...]:
        pass

    @property
    @abstractmethod
    def table_odds_setting(self) -> str:
        pass

    @property
    @abstractmethod
    def key_number(self) -> int:
        pass

    @staticmethod
    @abstractmethod
    def by_number(number: int, bet_amount: float) -> "BaseOdds":
        pass

    def get_base_bets(self, player: "Player") -> list["AllowsOdds"]:
        allows_odds_bets = [x for x in player.bets_on_table if isinstance(x, AllowsOdds)]
        bets_of_type = [x for x in allows_odds_bets if isinstance(x, tuple(self.base_bet_types))]
        base_bets = [x for x in bets_of_type
                     if x.get_winning_numbers(player.table) == self.winning_numbers]
        return base_bets

    def get_max_odds(self, table: "Table") -> int:
        return table.settings[self.table_odds_setting][self.key_number]

    def get_max_bet(self, player: "Player") -> float:
        base_bet_amount = sum(x.bet_amount for x in self.get_base_bets(player))
        max_odds = self.get_max_odds(player.table)
        return base_bet_amount * max_odds

    def allowed(self, player: "Player") -> bool:
        return self.get_max_bet(player) >= self.bet_amount

    def __hash__(self) -> int:
        return hash((type(self), self.bet_amount))

    @property
    @abstractmethod
    def payout_ratio(self) -> typing.SupportsFloat:
        pass

    def get_payout_ratio(self, table: "Table") -> float:
        return float(self.payout_ratio)


class AllowsOdds(WinningLosingNumbersBet, ABC):
    @abstractmethod
    def get_odds_bet(self, bet_amount: typing.SupportsFloat, table: "Table") -> BaseOdds:
        pass

    def get_payout_ratio(self, table: "Table") -> float:
        return 1.0


class PassLine(AllowsOdds):
    def get_odds_bet(self, bet_amount: typing.SupportsFloat, table: "Table") -> "Odds":
        if table.point.number is not None:
            return Odds.by_number(table.point.number, bet_amount)
        else:
            raise ValueError

    def get_winning_numbers(self, table: "Table") -> list[int]:
        if table.point.number is None:
            return [7, 11]
        return [table.point.number]

    def get_losing_numbers(self, table: "Table") -> list[int]:
        if table.point.number is None:
            return [2, 3, 12]
        return [7]

    def get_status(self, table: "Table") -> str | None:
        if table.point.status == 'Off' and table.last_roll in (4, 5, 6, 8, 9, 10):
            return None
        return super().get_status(table)

    def is_removable(self, player: "Player") -> bool:
        if player.table.point.status is 'On':
            return False
        return True

    def allowed(self, player: "Player") -> bool:
        if player.table.point.status == 'Off':
            return True
        return False

    def __hash__(self) -> int:
        return hash((PassLine, self.bet_amount))


class Come(AllowsOdds):
    def __init__(self, bet_amount: typing.SupportsFloat, point: int | None = None):
        super().__init__(bet_amount)
        self.point = point
        self._status: str | None = None

    def get_winning_numbers(self, table: "Table") -> list[int]:
        if self.point is None:
            return [7, 11]
        return [self.point]

    def get_losing_numbers(self, table: "Table") -> list[int]:
        if self.point is None:
            return [2, 3, 12]
        return [7]

    def get_status(self, table: "Table") -> str | None:
        return self._status

    def update(self, table: "Table") -> None:
        if self.point is None and table.dice.total in (4, 5, 6, 8, 9, 10):
            self.point = table.dice.total
        else:
            self._status = super().get_status(table)

    def is_removable(self, player: "Player") -> bool:
        if self.point is not None:
            return False
        return True

    def allowed(self, player: "Player") -> bool:
        if player.table.point.status == 'On':
            return True
        return False

    def already_placed(self, player: "Player") -> bool:
        return player.has_bets_by_type(type(self), point=self.point)

    def get_odds_bet(self, bet_amount: typing.SupportsFloat, table: "Table") -> "Odds":
        if self.point is not None:
            return Odds.by_number(self.point, bet_amount)
        else:
            raise ValueError

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Bet):
            return isinstance(other, type(self)) and \
                   other.bet_amount == self.bet_amount and \
                   other.point == self.point
        else:
            raise NotImplementedError

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(bet_amount={self.bet_amount}, point={self.point})'

    def __hash__(self) -> int:
        return hash((Come, self.bet_amount, self.point))

"""
Passline/Come bet odds
"""


class Odds(BaseOdds, ABC):
    base_bet_types = (PassLine, Come)
    table_odds_setting = 'max_odds'
    losing_numbers: list[int] = [7]

    @property
    def key_number(self) -> int:
        return self.winning_numbers[0]

    @staticmethod
    def by_number(number: int, bet_amount: typing.SupportsFloat) -> "Odds":
        return {4: Odds4, 5: Odds5, 6: Odds6, 8: Odds8, 9: Odds9, 10: Odds10}[number](bet_amount)


class Odds4(Odds):
    winning_numbers: list[int] = [4]
    payout_ratio: float = 2 / 1


class Odds5(Odds):
    winning_numbers: list[int] = [5]
    payout_ratio: float = 3 / 2


class Odds6(Odds):
    winning_numbers: list[int] = [6]
    payout_ratio: float = 6 / 5


class Odds8(Odds):
    winning_numbers: list[int] = [8]
    payout_ratio: float = 6 / 5


class Odds9(Odds):
    winning_numbers: list[int] = [9]
    payout_ratio: float = 3 / 2


class Odds10(Odds):
    winning_numbers: list[int] = [10]
    payout_ratio: float = 2 / 1


"""
Place Bets on 4,5,6,8,9,10
"""


class Place(StaticWinningLosingNumbersBet, ABC):
    losing_numbers: int = [7]

    def update(self, table: "Table") -> None:
        # place bets are inactive when point is "Off"
        if table.point == "On":
            super().update(table)

    @staticmethod
    def by_number(number: int, bet_amount: float) -> "Place":
        bet_type = {4: Place4,
                    5: Place5,
                    6: Place6,
                    8: Place8,
                    9: Place9,
                    10: Place10}[number]
        return bet_type(bet_amount)

    @property
    @abstractmethod
    def payout_ratio(self) -> float:
        pass

    def get_payout_ratio(self, table: "Table") -> float:
        return self.payout_ratio

    def __hash__(self) -> int:
        return hash((type(self), self.bet_amount))


class Place4(Place):
    payout_ratio: float = 9 / 5
    winning_numbers: list[int] = [4]


class Place5(Place):
    payout_ratio: float = 7 / 5
    winning_numbers: list[int] = [5]


class Place6(Place):
    payout_ratio: float = 7 / 6
    winning_numbers: list[int] = [6]


class Place8(Place):
    payout_ratio: float = 7 / 6
    winning_numbers: list[int] = [8]


class Place9(Place):
    payout_ratio: float = 7 / 5
    winning_numbers: list[int] = [9]


class Place10(Place):
    payout_ratio: float = 9 / 5
    winning_numbers: list[int] = [10]


"""
Field bet
"""


class OneRollBet(StaticWinningLosingNumbersBet, ABC):
    """WinningLosingNumbersBet where if the number isn't in the winning_numbers,
    it is in the losing_numbers."""
    @property
    def losing_numbers(self) -> list[int]:
        return [x for x in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] if x not in self.winning_numbers]

    def __hash__(self) -> list[int]:
        return hash((type(self), self.winning_numbers, self.bet_amount))


class Field(OneRollBet):
    def get_payout_ratio(self, table: "Table") -> float:
        if table.dice.total in table.settings['field_payouts']:
            return float(table.settings['field_payouts'][table.dice.total])
        return 0.0

    @property
    def winning_numbers(self) -> list[int]:
        return [2, 3, 4, 9, 10, 11, 12]


"""
Don't pass and Don't come bets
"""


class DontPass(AllowsOdds):
    def get_winning_numbers(self, table: "Table") -> list[int]:
        if table.point.number is None:
            return [2, 3]
        return [7]

    def get_losing_numbers(self, table: "Table") -> list[int]:
        if table.point.number is None:
            return [7, 11]
        return [table.point.number]

    def allowed(self, player: "Player") -> bool:
        if player.table.point.status == 'Off':
            return True
        return False

    def get_status(self, table: "Table") -> str | None:
        if table.point.status is None and table.dice.total in (4, 5, 6, 8, 9, 10):
            return None
        return super().get_status(table)

    def get_odds_bet(self, bet_amount: typing.SupportsFloat, table: "Table") -> "LayOdds":
        return LayOdds.by_number(table.point.number, bet_amount)

    def __hash__(self) -> int:
        return hash((DontPass, self.bet_amount))


class DontCome(AllowsOdds):
    def __init__(self, bet_amount: typing.SupportsFloat, point: int | None = None) -> None:
        super().__init__(bet_amount)
        self.point = point
        self._status = None

    def get_winning_numbers(self, table: "Table") -> list[int]:
        if self.point is None:
            return [2, 3]
        return [7]

    def get_losing_numbers(self, table: "Table") -> list[int]:
        if self.point is None:
            return [7, 11]
        return [self.point]

    def update(self, table: "Table") -> None:
        if self.point is None and table.dice.total in (4, 5, 6, 8, 9, 10):
            self.point = table.dice.total
        else:
            self._status = super().get_status(table)

    def allowed(self, player: "Player") -> bool:
        if player.table.point.status == 'On':
            return True
        return False

    def get_status(self, table: "Table") -> str | None:
        return self._status

    def get_odds_bet(self, bet_amount: typing.SupportsFloat, table: "Table") -> "LayOdds":
        return LayOdds.by_number(self.point, bet_amount)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Bet):
            return isinstance(other, type(self)) and \
                   self.bet_amount == other.bet_amount and \
                   self.point == other.point

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(bet_amount={self.bet_amount}, point={self.point})'

    def already_placed(self, player: "Player") -> bool:
        return player.has_bets_by_type(type(self), point=self.point)

    def __hash__(self) -> int:
        return hash((type(self), self.bet_amount))


"""
Don't pass/Don't come lay odds
"""


class LayOdds(BaseOdds, ABC):
    base_bet_types: typing.Type[AllowsOdds] = (DontPass, DontCome)
    table_odds_setting: str = 'max_dont_odds'
    winning_numbers: int = [7]

    @property
    def key_number(self) -> int:
        return self.losing_numbers[0]

    @staticmethod
    def by_number(number: int, bet_amount: float) -> "LayOdds":
        return {4: LayOdds4,
                5: LayOdds5,
                6: LayOdds6,
                8: LayOdds8,
                9: LayOdds9,
                10: LayOdds10}[number](bet_amount)


class LayOdds4(LayOdds):
    losing_numbers: int = [4]
    payout_ratio: float = 1 / 2


class LayOdds5(LayOdds):
    losing_numbers: list[int] = [5]
    payout_ratio: float = 2 / 3


class LayOdds6(LayOdds):
    losing_numbers: list[int] = [6]
    payout_ratio: float = 5 / 6


class LayOdds8(LayOdds):
    losing_numbers: list[int] = [8]
    payout_ratio: float = 5 / 6


class LayOdds9(LayOdds):
    losing_numbers: list[int] = [9]
    payout_ratio: float = 2 / 3


class LayOdds10(LayOdds):
    losing_numbers: list[int] = [10]
    payout_ratio: float = 1 / 2


"""
Center-table Bets
"""


class StaticPayoutOneRollBet(OneRollBet):
    @property
    @abstractmethod
    def payout_ratio(self):
        pass

    def get_payout_ratio(self, table: "Table") -> float:
        return self.payout_ratio


class Any7(StaticPayoutOneRollBet):
    payout_ratio: int = 4
    winning_numbers: int = [7]


class Two(StaticPayoutOneRollBet):
    payout_ratio: int = 30
    winning_numbers: int = [2]


class Three(StaticPayoutOneRollBet):
    payout_ratio: int = 15
    winning_numbers: int = [3]


class Yo(StaticPayoutOneRollBet):
    payout_ratio: int = 15
    winning_numbers: int = [11]


class Boxcars(StaticPayoutOneRollBet):
    payout_ratio: int = 30
    winning_numbers: int = [12]


class AnyCraps(StaticPayoutOneRollBet):
    payout_ratio: int = 7
    winning_numbers: list[int] = [2, 3, 12]


class CAndE(OneRollBet):
    winning_numbers: list[int] = [2, 3, 11, 12]

    def get_payout_ratio(self, table: "Table") -> float:
        if table.dice.total in [2, 3, 12]:
            return 3.0
        elif table.dice.total in [11]:
            return 7.0
        else:
            raise NotImplementedError


class HardWay(Bet, ABC):
    def __init__(self, bet_amount: float) -> None:
        super().__init__(bet_amount)

    @property
    @abstractmethod
    def number(self) -> int:
        pass

    @property
    def winning_result(self) -> list[int]:
        return [self.number / 2, self.number / 2]

    def get_payout_ratio(self, table: "Table") -> float:
        return float(self.payout_ratio)

    def get_status(self, table: "Table") -> str | None:
        if table.dice.result == self.winning_result:
            return "win"
        elif table.dice.total in [self.number, 7]:
            return "lose"
        return None

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Bet) and not isinstance(other, type(self)):
            return False
        elif isinstance(other, type(self)):
            return self.number == other.number and self.bet_amount == other.bet_amount

    def __hash__(self) -> int:
        return hash((type(self), self.number, self.bet_amount))


def _hard_way_type_factory(number: int, payout_ratio: typing.SupportsFloat):
    __annotations__ = {'payout_ratio': int, 'number': int}
    __doc__ = f"""A HardWay bet on the number {number} with a payout ratio of {payout_ratio}.
    For this HardWay bet to win the dice have to both land on {number / 2}. The player loses 
    if the dice land on {number} with anything other than {number / 2} or if the dice land on 
    7."""
    attributes = {'payout_ratio': payout_ratio,
                  'number': number,
                  '__doc__': __doc__,
                  '__annotations__': __annotations__}
    return type(f'Hard{number}', (HardWay, ), attributes)


class Hard4(HardWay):
    payout_ratio: int = 7
    number: int = 4


class Hard6(HardWay):
    payout_ratio: int = 9
    number: int = 6


class Hard8(HardWay):
    payout_ratio: int = 9
    number: int = 8


class Hard10(HardWay):
    payout_ratio: int = 7
    number: int = 10


class Fire(Bet):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount)
        self.bet_amount: float = bet_amount
        self.points_made: list[int] = []
        self.current_point: int | None = None
        self.new_point_made: bool = False

    def get_status(self, table: "Table") -> str | None:
        if self.new_point_made and len(self.points_made) in table.settings['fire_points']:
            return "win"
        elif self.current_point is not None and table.dice.total == 7:
            return "lose"
        return None

    def should_remove(self, table: "Table") -> bool:
        if len(self.points_made) == 6 or self.get_status(table) == "lose":
            return True
        return False

    def update(self, table: "Table") -> None:
        self.new_point_made = False
        if self.current_point is None and table.dice.total in (4, 5, 6, 8, 9, 10):
            self.current_point = table.dice.total
        elif self.current_point is not None and self.current_point == table.dice.total:
            self.point_made(table)

    def point_made(self, table: "Table") -> None:
        if table.dice.total not in self.points_made:
            self.new_point_made = True
            self.points_made = self.points_made + [table.dice.total]
        self.current_point = None

    def allowed(self, player: "Player") -> bool:
        return player.table.new_shooter

    def get_payout_ratio(self, table: "Table") -> float:
        if len(self.points_made) in table.settings['fire_points']:
            return float(table.settings['fire_points'][len(self.points_made)])
        else:
            raise NotImplementedError

    def __eq__(self, other: Bet) -> bool:
        if isinstance(other, Bet) and not isinstance(other, type(self)):
            return False
        elif isinstance(other, type(self)):
            return self.bet_amount == other.bet_amount and \
                self.points_made == other.points_made

    def __hash__(self) -> int:
        return hash((Fire, self.bet_amount, tuple(self.points_made)))
