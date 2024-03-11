from dataclasses import dataclass
from crapssim.bet import BetStatus
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

        self.bet_stats = BetStats()

        self.bet_strategy = bet_strategy
        self.name = name
        self.bets_on_table = []
        self.total_bet_amount = 0
        self.logger = LogMixin(verbose)
        self.verbose = verbose
    
    def __repr__(self) -> str:
        return f"{self.name}: bank: ${self.bankroll_finance.current} bets:${self.total_bet_amount}"

    def __str__(self) -> str:
        return f"{self.name} - bets:{self.total_bet_amount}"

    def bet(self, bet_object):
        if not self.has_matching_bet(bet_object):
            if self.bankroll_finance.current >= bet_object.bet_amount:
                self.bet_stats.biggest_bet = max(self.bet_stats.biggest_bet, bet_object.bet_amount)
                self.bankroll_finance.current = round(self.bankroll_finance.current - bet_object.bet_amount, 2)
                self.bets_on_table.append(bet_object)
                # TODO: This isn't correct!!
                self.total_bet_amount += bet_object.bet_amount

    def remove(self, bet_object):
        if bet_object in self.bets_on_table:
            self.bankroll_finance.current += bet_object.bet_amount
            self.bets_on_table.remove(bet_object)
            self.total_bet_amount -= bet_object.bet_amount
    
    def has_matching_bet(self, bet_object):
        for current_bet in self.bets_on_table:
            if bet_object.name == current_bet.name and bet_object.subname == current_bet.subname:
                return True
        return False

    def has_bet(self, *bets_to_check):
        """ returns True if bets_to_check and self.bets_on_table has at least one thing in common """
        bet_names = {b.name for b in self.bets_on_table}
        return bool(bet_names.intersection(bets_to_check))

    def has_bet_type(self, bet_type):
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

    def num_bet(self, *bets_to_check):
        """ returns the total number of bets in self.bets_on_table that match bets_to_check """
        bet_names = [b.name for b in self.bets_on_table]
        return sum([i in bets_to_check for i in bet_names])

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
                    self.total_bet_amount -= bet_on_table.bet_amount
                    self.bets_on_table.remove(bet_on_table)
                case BetStatus.LOSE:
                    self.bet_stats.biggest_loss = max(bet_on_table.bet_amount, self.bet_stats.biggest_loss)
                    self.total_bet_amount -= bet_on_table.bet_amount
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
        return info

@dataclass
class BankRoll():
    starting = 0
    largest = 0
    current = 0
    smallest = 0
    target = 0

@dataclass
class BetStats():
    biggest_win = 0
    biggest_loss = 0
    biggest_bet = 0