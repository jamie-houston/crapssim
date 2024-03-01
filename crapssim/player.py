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

    Attributes
    ----------
    bets_on_table : list
        List of betting objects for the player
    total_bet_amount : int
        Sum of bet value for the player
    """

    def __init__(self, bankroll, bet_strategy=None, name="Player", verbose=False):
        self.bankroll = bankroll
        self.bet_strategy = bet_strategy
        self.name = name
        self.bets_on_table = []
        self.total_bet_amount = 0
        self.verbose = verbose
        self.biggest_win = 0
        self.biggest_loss = 0
        self.biggest_bet = 0

    def bet(self, bet_object):
        if not self.has_matching_bet(bet_object):
            # don't add duplicate bet
            if self.bankroll >= bet_object.bet_amount:
                if self.biggest_bet < bet_object.bet_amount:
                    self.biggest_bet = bet_object.bet_amount
                self.bankroll -= bet_object.bet_amount
                self.bets_on_table.append(bet_object)
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
            status, win_amount = b._update_bet(table_object, dice_object)
            win_amount = int(win_amount)

            if status == "win":
                if win_amount > self.biggest_win:
                    self.biggest_win = win_amount
                self.bankroll += win_amount + b.bet_amount
                self.total_bet_amount -= b.bet_amount
                self.bets_on_table.remove(b)
                if self.verbose:
                    print(f"{self.name} won ${win_amount} on {b} bet!")
            elif status == "lose":
                if b.bet_amount > self.biggest_loss:
                    self.biggest_loss = b.bet_amount
                self.total_bet_amount -= b.bet_amount
                self.bets_on_table.remove(b)
                if self.verbose:
                    print(f"{self.name} lost ${b.bet_amount} on {b} bet.")
            elif status == "push":
                self.bankroll += b.bet_amount
                self.total_bet_amount -= b.bet_amount
                self.bets_on_table.remove(b)
                if self.verbose:
                    print(f"{self.name} pushed ${b.bet_amount} on {b} bet.")

            info[b.name] = {"status": status, "win_amount": win_amount}
        return info
