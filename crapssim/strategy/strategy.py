from enum import Enum
from typing import final

from crapssim.bet import BetStatus

"""
Various betting strategies that are based on conditions of the CrapsTable.
Each strategy must take a table and a player_object, and implicitly 
uses the methods from the player object.
"""

"""
Fundamental Strategies
"""


class RollEvent(Enum):
    BEFORE_ROLL_CALLBACK = "before_roll_callback"
    NEW_SHOOTER = "on_new_shooter"
    COMING_OUT = "on_coming_out"
    POINT_SET = "on_point_set"
    POINT_HIT = "on_point_hit"
    SEVEN_OUT = "on_seven_out"
    ACTIVE_POINT = "on_active_point"
    ANY_STATUS = "on_any_status"
    AFTER_ROLL_CALLBACK = "after_roll_callback"


class BetEvent(Enum):
    BEFORE_BET_RESULT = "before_bet_result"
    ON_WIN = "on_win"
    ON_LOSS = "on_loss"
    ON_PUSH = "on_push"
    AFTER_BET_RESULT = "after_bet_result"


class Strategy:
    """
    Bet based on status.

    You can either implement handle_roll_events and use whichever even you want
    Or implement one of the below methods

    Status of roll in chronological order:
    0. before_roll_callback - before any callbacks
    1. on_new_shooter - first roll of shooter
    2. on_coming_out - point not set
    3. on_point_set - first roll after point is set
    4. on_point_hit - first roll after point is hit
    5. on_seven_out - seven out
    6. on_active_point - point is set
    7. on_any_status - Any time in roll
    8. after_roll_callback - after all callbacks

    Bet results - Called for each existing bet on the table
    0. before_bet_result
    1. on_win - win
    2. on_loss - loss
    3. on_push - no change
    4. after_bet_result



    """

    def __init__(self, unit=5, verbose=False):
        self.base_unit = unit
        self.verbose = verbose
        self.strategies = []

    def __call__(self, other):
        self.strategies.append(other)

    @final
    def update_bets(self, player, table, unit, strat_info=None):
        """
        This is called before every roll to determine bets to place
        """
        last_bets = table.bet_update_info and table.bet_update_info.get(player)
        self.__handle_bet_callbacks(player, table, last_bets)

        self.__handle_roll_callbacks(player, table)

    @property
    def unit(self):
        """
        To change the base unit, override this method
        :return:
        """
        return self.base_unit

    def handle_roll_event(self, roll_event, *args):
        def run_method(s):
            method = getattr(s, roll_event.value, None)
            if method:
                method(*args)  # Call the method directly if it exists

        if len(self.strategies):
            [run_method(s) for s in self.strategies]
        else:
            run_method(self)

    def __handle_roll_callbacks(self, player, table):
        self.handle_roll_event(RollEvent.BEFORE_ROLL_CALLBACK, player, table)
        if table.point.is_on():
            if table.last_roll == table.point.number:
                self.handle_roll_event(RollEvent.POINT_SET, player, table, table.last_roll)
            self.handle_roll_event(RollEvent.ACTIVE_POINT, player, table)
        else:
            if table.last_roll is None:
                self.handle_roll_event(RollEvent.NEW_SHOOTER, player, table)
            elif table.last_roll == 7:
                self.handle_roll_event(RollEvent.SEVEN_OUT, player, table)
            elif table.last_roll not in [2, 3, 11, 12]:
                self.handle_roll_event(RollEvent.POINT_HIT, player, table, table.last_roll)
            self.handle_roll_event(RollEvent.COMING_OUT, player, table)
        self.handle_roll_event(RollEvent.ANY_STATUS, player, table)
        self.handle_roll_event(RollEvent.AFTER_ROLL_CALLBACK, player, table)

    def __handle_bet_callbacks(self, player, table, last_bets):
        if last_bets is not None:
            for bet, bet_info in last_bets.items():
                self.handle_roll_event(BetEvent.BEFORE_BET_RESULT, player, table, bet_info)
                match bet_info.status:
                    case BetStatus.PUSH:
                        self.handle_roll_event(BetEvent.ON_PUSH, player, table, bet_info)
                    case BetStatus.WIN:
                        self.handle_roll_event(BetEvent.ON_WIN, player, table, bet_info)
                    case BetStatus.LOSE:
                        self.handle_roll_event(BetEvent.ON_LOSS, player, table, bet_info)
                self.handle_roll_event(BetEvent.AFTER_BET_RESULT, player, table, bet_info)
