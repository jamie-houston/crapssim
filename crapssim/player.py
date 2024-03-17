import decimal
from dataclasses import dataclass
from crapssim.bet import Bet, BetStatus, Odds
from icecream import ic

from crapssim.logging import LogMixin


class Player(object):
    """
    Player standing at the craps table

    Parameters
    ----------
    bankroll : float
        Starting amount of cash for the player, will be updated during play
    bet_strategy : function(table, player, unit=5)
        A function that implements a particular betting strategy.  See betting_strategies.py
    name : string, optional (default = "Player")
        Name of the player
    target_bankroll : Desired amount to get to.  Once reached, roll is successful

    Attributes
    ----------
    bets_on_table : list
        List of betting objects for the player
    total_bet_amount : int
        Sum of bet value for the player
    """

    # ic.disable()
    def __init__(self, bankroll, bet_strategy=None, name="Player", target_bankroll=None, verbose=False):
        self.bankroll_finance = BankRoll()
        self.bankroll_finance.starting = bankroll
        self.bankroll_finance.target = target_bankroll
        self.bankroll_finance.current = bankroll
        self.bankroll_finance.smallest = bankroll
        self.bankroll_finance.largest = bankroll
        self.continue_rolling = True
        self.bet_stats = BetStats()

        self.bet_strategy = bet_strategy
        self.name = name
        self.bets_on_table = []
        self.logger = LogMixin(verbose)
        self.verbose = verbose

    def __repr__(self) -> str:
        return f"{self.name}: bank: ${self.bankroll_finance.current} bets:${self.total_bet_amount}"

    def __str__(self) -> str:
        return f"{self.name} - bets:{self.total_bet_amount}"

    total_bet_amount = property(
        fget=lambda self: sum(b.bet_amount for b in self.bets_on_table),
    )

    def bet(self, bet_object):
        if not self.has_matching_bet(bet_object):
            if self.bankroll_finance.current >= bet_object.bet_amount:
                self.bet_stats.biggest_bet = max(self.bet_stats.biggest_bet, bet_object.bet_amount)
                self.bankroll_finance.current = round(self.bankroll_finance.current - bet_object.bet_amount, 2)
                self.bets_on_table.append(bet_object)

    def add_odds(self, bet_type: Bet, amount, number=None):
        # if bet_type not in self.bets_on_table:
        #     self.logger.log(f"Cannot put odds on {bet_type}.  No bets found.")
        # else:
        #     current_bet = [bet for bet in self.bets_on_table if bet.is_bet_type(bet_type)][0]
        #     if len(current_bet) == 1:
        self.bet(Odds(amount, bet_type))

    def remove(self, bet_object):
        if bet_object in self.bets_on_table:
            self.bankroll_finance.current += bet_object.bet_amount
            self.bets_on_table.remove(bet_object)

    def has_matching_bet(self, bet_object):
        for current_bet in self.bets_on_table:
            if bet_object.name == current_bet.name and bet_object.subname == current_bet.subname:
                return True
        return False

    def has_bet(self, *bets_to_check):
        """ returns True if bets_to_check and self.bets_on_table has at least one thing in common """
        bet_names = {b.name for b in self.bets_on_table}
        return bool(bet_names.intersection(bets_to_check))

    def has_bet_type(self, bet_type: Bet):
        for bet in self.bets_on_table:
            if bet.is_bet_type(bet_type):
                return True
        return False

    def get_bet(self, bet_name, bet_subname=""):
        """returns first betting object matching bet_name and bet_subname.
        If bet_subname="Any", returns first betting object matching bet_name"""
        if bet_subname == "Any":
            bet_name_list = [b.name for b in self.bets_on_table]
            ind = bet_name_list.index(bet_name)
        else:
            bet_name_list = [[b.name, b.subname] for b in self.bets_on_table]
            ind = bet_name_list.index([bet_name, bet_subname])
        return self.bets_on_table[ind]

    def get_bet_type(self, bet_type):
        for bet in self.bets_on_table:
            if bet.__class__ == bet_type:
                return bet

    def number_of_bets_by_type(self, bet_type):
        # TODO: This probably don't check hierarchical class
        # Place6 should be true for Place, Come9 for Come, etc
        """ returns the total number of bets in self.bets_on_table that match the bet_type """
        number_of_bets = 0
        for bet in self.bets_on_table:
            if bet.__class__ == bet_type:
                number_of_bets += 1

        return number_of_bets

    def remove_if_present(self, bet_name, bet_subname=""):
        if self.has_bet(bet_name):
            self.remove(self.get_bet(bet_name, bet_subname))

    def _add_strategy_bets(self, table, *args, **kwargs):
        """ Implement the given betting strategy """
        return self.bet_strategy(self, table, *args, **kwargs)

    def _update_bet(self, table_object, dice_object):
        info = {}
        for bet_on_table in self.bets_on_table[:]:
            bet_result = bet_on_table._update_bet(table_object, dice_object)
            bet_result.win_amount = round(bet_result.win_amount, 2)

            match bet_result.status:
                case BetStatus.WIN:
                    self.bet_stats.biggest_win = max(bet_result.win_amount, self.bet_stats.biggest_win)
                    self.bankroll_finance.current += bet_result.win_amount + bet_on_table.bet_amount
                    if bet_on_table.remove_on_win:
                        self.bets_on_table.remove(bet_on_table)
                case BetStatus.LOSE:
                    self.bet_stats.biggest_loss = max(bet_on_table.bet_amount, self.bet_stats.biggest_loss)
                    self.bets_on_table.remove(bet_on_table)
                case BetStatus.PUSH:
                    pass

            bet_result.__dict__.update(bet_on_table.__dict__)

            info[bet_on_table] = bet_result

        self.bankroll_finance.largest = max(self.bankroll_finance.largest, self.bankroll_finance.current)
        self.bankroll_finance.smallest = min(self.bankroll_finance.smallest, self.bankroll_finance.current)
        winning_bets = []
        losing_bets = []
        for bet_on_table, result in info.items():
            if result.status == BetStatus.WIN:
                winning_bets.append(f"${result.win_amount} on {bet_on_table}")
            elif result.status == BetStatus.LOSE:
                losing_bets.append(f"${result.bet_amount} on {bet_on_table}")
        if len(winning_bets):
            self.logger.log_green(f"{self.name} WON " + ", ".join(winning_bets))
        if len(losing_bets):
            self.logger.log_red(f"{self.name} LOST " + ", ".join(losing_bets))

        if self.bankroll_finance.target is not None and self.bankroll_finance.target <= self.bankroll_finance.current:
            self.continue_rolling = False
        return info

class MoneyField:
    def __init__(self, *, default):
        self._default = default

    def __set_name__(self, owner, name):
        self._name = "_" + name

    def __get__(self, obj, type):
        if obj is None:
            return self._default

        return getattr(obj, self._name, self._default)

    def __set__(self, obj, value):
        setattr(obj, self._name, round(value, 2))

@dataclass
class BankRoll:
    starting = MoneyField(default=0)
    largest = MoneyField(default=0)
    current = MoneyField(default=0)
    smallest = MoneyField(default=0)
    target = MoneyField(default=0)


@dataclass
class BetStats:
    biggest_win = 0
    biggest_loss = 0
    biggest_bet = 0
