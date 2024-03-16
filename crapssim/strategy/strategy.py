from enum import Enum
from crapssim.bet import BetStatus
from crapssim.strategy.alternative import AlternativeStrategy

"""
Various betting strategies that are based on conditions of the CrapsTable.
Each strategy must take a table and a player_object, and implicitly 
uses the methods from the player object.
"""

"""
Fundamental Strategies
"""


class RollStatus(Enum):
    NEW_SHOOTER = "on_new_shooter",
    COMING_OUT = "on_coming_out",
    POINT_SET = "on_point_set",
    POINT_HIT = "on_point_hit",
    SEVEN_OUT = "on_seven_out",
    ACTIVE_POINT = "on_active_point",
    ANY_STATUS = "on_any_status",


class Strategy:
    """
    Bet based on status.
    Overwrite any method you want to use
    Do NOT overwrite update bets unless you don't want the other methods to work

    Status of roll in chronological order:
    1. on_new_shooter - first roll of shooter
    2. on_coming_out - point not set
    3. on_point_set - first roll after point is set
    4. on_point_hit - first roll after point is hit
    5. on_seven_out - seven out
    6. on_active_point - point is set
    7. on_any_status - Any time in roll

    Bet results - Called for each existing bet on the table
    1. before_bet_result
    1. on_win - win
    2. on_loss - loss
    3. on_push - no change
    4. after_bet_result



    """

    def __init__(self, unit=5, verbose=False, alternatives = None):
        self.unit = unit
        self.verbose = verbose
        self.alternatives = alternatives

    def update_bets(self, player, table, unit, strat_info=None):
        last_bets = table.bet_update_info and table.bet_update_info.get(player)
        self.__handle_bet_callbacks(player, table, last_bets)

        self.__handle_roll_callbacks(player, table)

    def __handle_roll_callbacks(self, player, table):
        self.before_roll_callback(player, table, table.last_roll)
        if table.point.is_on():
            if table.last_roll == table.point.number:
                self.on_point_set(player, table, table.last_roll)
            self.on_active_point(player, table)
        else:
            if table.last_roll is None:
                self.on_new_shooter(player, table)
            elif table.last_roll == 7:
                self.on_seven_out(player, table)
            elif table.last_roll not in [2, 3, 11, 12]:
                self.on_point_hit(player, table, table.last_roll)
            self.on_coming_out(player, table)
        self.on_any_status(player, table)

    def __handle_bet_callbacks(self, player, table, last_bets):
        if last_bets is not None:
            for bet, bet_info in last_bets.items():
                self.before_bet_result(player, table, bet_info)
                match bet_info.status:
                    case BetStatus.PUSH:
                        self.on_push(player, table, bet_info)
                    case BetStatus.WIN:
                        self.on_win(player, table, bet_info)
                    case BetStatus.LOSE:
                        self.on_loss(player, table, bet_info)
                self.after_bet_result(player, table, bet_info)

    def before_bet_result(self, player, table, bet_info):
        # Called before any bet result
        pass

    def after_bet_result(self, player, table, bet_info):
        # Called with any bet result
        pass

    def on_win(self, player, table, winning_bet):
        # Called with any winning bet
        pass

    def on_loss(self, player, table, losing_bet_info):
        # Called with any losing bet
        pass

    def on_push(self, player, table, bet_info):
        # Called with any push bet
        pass

    def on_seven_out(self, player, table):
        # called after 7 out
        pass

    def before_roll_callback(self, player, table, last_roll):
        # Called before any roll
        pass

    def on_point_set(self, player, table, last_roll):
        # When the point starts
        pass

    def on_point_hit(self, player, table, last_roll):
        pass

    def on_new_shooter(self, player, table):
        # New shooter coming out
        pass

    def on_any_status(self, player, table):
        pass

    def on_active_point(self, player, table):
        pass

    def on_coming_out(self, player, table):
        # When the point is off
        pass
