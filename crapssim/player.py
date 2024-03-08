from crapssim.bet import BetStatus
from icecream import ic


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

    ic.disable()
    def __init__(self, bankroll, bet_strategy=None, name="Player", target_bankroll=None, verbose=False):
        self.bankroll = bankroll
        self.starting_bankroll = bankroll
        self.target_bankroll = target_bankroll
        self.bet_strategy = bet_strategy
        self.name = name
        self.bets_on_table = []
        self.total_bet_amount = 0
        self.verbose = verbose
        self.biggest_win = 0
        self.biggest_loss = 0
        self.biggest_bet = 0
        self.reached_target = False
    
    def __repr__(self) -> str:
        return f"{self.name}: bank: ${self.bankroll} bets:${self.total_bet_amount}"

    def __str__(self) -> str:
        return f"{self.name} - bets:{self.total_bet_amount}"

    def bet(self, bet_object):
        if not self.has_matching_bet(bet_object):
            # don't add duplicate bet
            if self.bankroll >= bet_object.bet_amount:
                if self.biggest_bet < bet_object.bet_amount:
                    self.biggest_bet = bet_object.bet_amount
                self.bankroll = round(self.bankroll - bet_object.bet_amount, 2)
                self.bets_on_table.append(bet_object)
                # TODO: This isn't correct!!
                self.total_bet_amount += bet_object.bet_amount

    def remove(self, bet_object):
        # TODO: add bet attribute for whether a bet can be removed and put condition in here
        if bet_object in self.bets_on_table:
            self.bankroll += bet_object.bet_amount
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
        for b in self.bets_on_table[:]:
            bet_result = b._update_bet(table_object, dice_object)
            bet_result.win_amount = round(bet_result.win_amount, 2)

            match bet_result.status:
                case BetStatus.WIN:
                    if bet_result.win_amount > self.biggest_win:
                        self.biggest_win = bet_result.win_amount
                    self.bankroll += bet_result.win_amount + b.bet_amount
                    self.total_bet_amount -= b.bet_amount
                    self.bets_on_table.remove(b)
                case BetStatus.LOSE:
                    if b.bet_amount > self.biggest_loss:
                        self.biggest_loss = b.bet_amount
                    self.total_bet_amount -= b.bet_amount
                    self.bets_on_table.remove(b)
                case BetStatus.PUSH:
                    self.bankroll += b.bet_amount
                    self.total_bet_amount -= b.bet_amount
            
            bet_result.__dict__.update(b.__dict__)


            info[b.name] = bet_result
        
        response = f"{self.name} :"
        for name, result in info.items():
            response += f"{result.status.value} ${result.bet_amount if result.win_amount == 0 else result.win_amount} on {name} |"
        if self.verbose:
            print(response)
        return info
