import copy
import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass

if typing.TYPE_CHECKING:
    from crapssim.table import Table, Player


@dataclass(frozen=True)
class BetResult:
    amount: float
    remove: bool

    @property
    def won(self) -> bool:
        return self.amount > 0

    @property
    def lost(self) -> bool:
        return self.amount < 0

    @property
    def pushed(self) -> bool:
        return self.amount == 0

    @property
    def bankroll_change(self) -> float:
        if self.won:
            return self.amount
        else:
            return 0


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
        self.amount: float = float(bet_amount)

    @abstractmethod
    def get_result(self, table: "Table") -> BetResult:
        pass

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

    def update_point(self, player: 'Player'):
        pass

    def get_hash_key(self) -> typing.Hashable:
        return self.get_placed_key(), self.amount

    def get_placed_key(self) -> typing.Hashable:
        return type(self)

    def already_placed_bets(self, player: "Player"):
        return [x for x in player.bets if x.get_placed_key() == self.get_placed_key()]

    def already_placed(self, player: "Player") -> bool:
        return len(self.already_placed_bets(player)) > 0

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Bet):
            return self.get_hash_key() == other.get_hash_key()
        raise NotImplementedError

    def __hash__(self) -> int:
        return hash(self.get_hash_key())

    def __repr__(self) -> str:
        return f'${self.amount} {self.__class__.__name__} {getattr(self, "point", "")}'

    def __add__(self, other: 'Bet') -> 'Bet':
        if isinstance(other, typing.SupportsFloat):
            bet_amount = self.amount - float(other)
        elif self.get_placed_key() == other.get_placed_key():
            bet_amount = self.amount + other.amount
        else:
            raise NotImplementedError
        new_bet = copy.copy(self)
        new_bet.amount = bet_amount
        return new_bet

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other: 'Bet') -> 'Bet':
        if isinstance(other, typing.SupportsFloat):
            bet_amount = self.amount - float(other)
        elif self.get_placed_key() == other.get_placed_key():
            bet_amount = self.amount - other.amount
        else:
            raise NotImplementedError
        new_bet = copy.copy(self)
        new_bet.amount = bet_amount
        return new_bet

    def __rsub__(self, other):
        return self.__sub__(other)


class WinningLosingNumbersBet(Bet, ABC):
    @abstractmethod
    def get_winning_numbers(self, table: "Table") -> list[int]:
        pass

    @abstractmethod
    def get_losing_numbers(self, table: "Table") -> list[int]:
        pass

    @abstractmethod
    def get_payout_ratio(self, table: "Table") -> float:
        pass

    def get_result(self, table: "Table") -> BetResult:
        if table.dice.total in self.get_winning_numbers(table):
            result_amount = self.get_payout_ratio(table) * self.amount + self.amount
            should_remove = True
        elif table.dice.total in self.get_losing_numbers(table):
            result_amount = -1 * self.amount
            should_remove = True
        else:
            result_amount = 0
            should_remove = False

        return BetResult(result_amount, should_remove)