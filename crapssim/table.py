import typing

from crapssim.dice import Dice
from .bet import Bet, BetResult
from .point import Point
from .strategy import Strategy, BetPassLine


class TableUpdate:
    """Object for processing a table after the dice has been rolled."""

    def run(self, table: 'Table',
            dice_outcome: typing.Iterable[int] | None = None,
            verbose: bool = False,
            update_after_roll = None):
        """Run through the roll logic of the table."""
        self.run_strategies(table)
        self.before_roll(table)
        self.update_table_stats(table)
        self.roll(table, dice_outcome, verbose)
        self.set_new_shooter(table)
        self.after_roll(table)
        self.update_bets(table, verbose)
        self.update_points(table, verbose)
        update_after_roll(table)

    @staticmethod
    def before_roll(table: 'Table'):
        table.last_roll = table.dice.total

    @staticmethod
    def roll(table: 'Table',
             fixed_outcome: typing.Iterable[int] | None = None,
             verbose: bool = False):
        if fixed_outcome is not None:
            table.dice.fixed_roll(fixed_outcome)
        else:
            table.dice.roll()
        if verbose:
            print("")
            print("Dice out!")
            print(f"Shooter rolled {table.dice.total} {table.dice.result}")

    @staticmethod
    def after_roll(table: 'Table'):
        for player in table.players:
            player.strategy.after_roll(player)

    @staticmethod
    def update_bets(table: 'Table', verbose=False):
        for player in table.players:
            player.update_bet(verbose=verbose)

    @staticmethod
    def update_table_stats(table: 'Table'):
        table.pass_rolls += 1
        if table.point == "On" and (table.dice.total == 7 or
                                    table.dice.total == table.point.number):
            table.pass_rolls = 0

    @staticmethod
    def set_new_shooter(table: 'Table'):
        if table.n_shooters == 0 or (table.point == "On" and table.dice.total == 7):
            table.new_shooter = True
            table.n_shooters += 1
        else:
            table.new_shooter = False

    @staticmethod
    def update_points(table: 'Table', verbose: bool):
        for player, bet in table.yield_player_bets():
            bet.update_point(player)
        table.point.update(table.dice)

        if verbose:
            print(f"Point is {table.point.status} ({table.point.number})")
            print(f"Total Player Cash is ${table.total_player_cash}")

    @staticmethod
    def run_strategies(table: 'Table'):
        for player in table.players:
            player.strategy.update_bets(player)


class Table:
    """
    Craps Table that contains Dice, Players, the Players' bets, and updates
    them accordingly.  Main method is run() which should simulate a craps
    table until a specified number of rolls plays out or all players run out
    of money.

    Attributes
    ----------
    players : list
        List of player objects at the table
    point : string
        The point for the table.  It is either "Off" when point is off or "On"
        when point is on.
    dice : Dice
        Dice for the table
    settings : dice[str, list[int]]
        Field payouts for the table
    pass_rolls : int
        Number of rolls for the current pass
    last_roll : int
        Total of the last roll for the table
    n_shooters : int
        How many shooters the table has had.
    new_shooter : bool
        Returns True if the previous shooters roll just ended and the next shooter hasn't shot.
    """

    def __init__(self) -> None:
        self.players: list[Player] = []
        self.point: Point = Point()
        self.dice: Dice = Dice()
        self.settings: dict[str, typing.Any] = {'field_payouts': {2: 2, 3: 1, 4: 1, 9: 1, 10: 1,
                                                                  11: 1, 12: 2},
                                                'fire_points': {4: 24, 5: 249, 6: 999},
                                                'max_odds': {4: 3, 5: 4, 6: 5, 8: 5, 9: 4, 10: 3},
                                                'max_dont_odds': {4: 6, 5: 6, 6: 6, 8: 6, 9: 6,
                                                                  10: 6}}
        self.pass_rolls: int = 0
        self.last_roll: int | None = None
        self.n_shooters: int = 0
        self.new_shooter: bool = True

    def yield_player_bets(self) -> typing.Generator[tuple['Player', 'Bet'], None, None]:
        for player in self.players:
            for bet in player.bets:
                yield player, bet

    def add_player(self, bankroll: typing.SupportsFloat = 100, strategy: Strategy = BetPassLine(5),
                   name: str = None) -> None:
        """ Add player object to the table

        Parameters
        ----------
        bankroll
            The players bankroll, defaults to 100.
        strategy
            The players strategy, defaults to passline.
        name
            The players name, if None defaults to "Player x" with x being the current number
            of players starting with 0 (ex. Player 0, Player 1, Player 2).

        """
        if name is None:
            name = f'Player {len(self.players)}'
        self.players.append(Player(table=self, bankroll=bankroll, bet_strategy=strategy, name=name))

    def _setup_run(self, verbose: bool) -> None:
        """
        Setup the table to run and ensure that there is at least one player.

        Parameters
        ----------
        verbose
            If True prints a welcome message and the initial players.
        """
        if verbose:
            print("Welcome to the Craps Table!")
        self.ensure_one_player()
        if verbose:
            print(f"Initial players: {[p.name for p in self.players]}")

    def run(self, max_rolls: int,
            max_shooter: float | int = float("inf"),
            verbose: bool = True,
            runout: bool = False,
            update_after_roll = None) -> None:
        """
        Runs the craps table until a stopping condition is met.

        Parameters
        ----------
        max_shooter : float | int
            Maximum number of shooters to run for
        max_rolls : int
            Maximum number of rolls to run for
        verbose : bool
            If true, print results from table during each roll
        runout : bool
            If true, continue past max_rolls until player has no more bets on the table
        """

        self._setup_run(verbose)

        continue_rolling = True
        while continue_rolling:
            TableUpdate().run(self, verbose=verbose, update_after_roll=update_after_roll)
            continue_rolling = self.should_keep_rolling(max_rolls, max_shooter, runout)

    def fixed_run(self, dice_outcomes: typing.Iterable[typing.Iterable], verbose: bool = False) \
            -> None:
        """
        Give a series of fixed dice outcome and run as if that is what was rolled.

        Parameters
        ----------
        dice_outcomes
            Iterable with two integers representing the dice faces.
        verbose
            If true, print results from table during each roll
        """
        self._setup_run(verbose=verbose)

        for dice_outcome in dice_outcomes:
            TableUpdate().run(self, dice_outcome, verbose=verbose)

    def should_keep_rolling(self, max_rolls: float | int, max_shooter: float | int,
                            runout: bool) -> bool:
        """
        Determines whether the program should keep running or not.

        Parameters
        ----------
        max_rolls
            Maximum number of rolls to run for
        max_shooter
            Maximum number of shooters to run for
        runout
            If true, continue past max_rolls until player has no more bets on the table

        Returns
        -------
        If True, the program should continue running. If False the program should stop running.
        """
        if runout:
            return (self.dice.n_rolls < max_rolls
                    and self.n_shooters <= max_shooter
                    and not any(x.strategy.completed(x) for x in self.players)
                    ) or self.player_has_bets
        else:
            return (
                    self.dice.n_rolls < max_rolls
                    and self.n_shooters <= max_shooter
                    and not any(x.strategy.completed(x) for x in self.players)
            )

    def ensure_one_player(self) -> None:
        """ Make sure there is at least one player at the table
        """
        if len(self.players) == 0:
            self.add_player()

    @property
    def player_has_bets(self) -> bool:
        """
        Returns whether any of the players on the table have any active bets.

        Returns
        -------
        True if any of the players have bets on the table, otherwise False.
        """
        return sum([len(p.bets) for p in self.players]) > 0

    @property
    def total_player_cash(self) -> float:
        """
        Returns the total sum of all players total_bet_amounts and bankroll.

        Returns
        -------
        The total sum of all players total_bet_amounts and bankroll.
        """
        return sum([p.total_cash for p in self.players])

    def get_player(self, player_name):
        return ([p for p in self.players if p.name == player_name] or None)[0]

    def __repr__(self) -> str:
        return f'{self.point} - {self.dice.total}'


class Player:
    """
    Player standing at the craps table

    Parameters
    ----------
    bankroll : typing.SupportsFloat
        Starting amount of cash for the player
    bet_strategy : function(table, player, unit=5)
        A function that implements a particular betting strategy.  See betting_strategies.py
    name : string, default = "Player"
        Name of the player

    Attributes
    ----------
    bankroll : typing.SupportsFloat
        Current amount of cash for the player
    name : str
        Name of the player
    bet_strategy :
        A function that implements a particular betting strategy. See betting_strategies.py.
    bets : list
        List of betting objects for the player
    """

    def __init__(self, table: Table,
                 bankroll: typing.SupportsFloat,
                 bet_strategy: Strategy = BetPassLine(5),
                 name: str = "Player"):
        self.bankroll: float = float(bankroll)
        self.strategy: Strategy = bet_strategy
        self.name: str = name
        self.bets: list[Bet] = []
        self._table: Table = table

    @property
    def total_bet_amount(self) -> float:
        return sum(x.amount for x in self.bets)

    @property
    def total_cash(self) -> float:
        return self.total_bet_amount + self.bankroll

    @property
    def table(self) -> Table:
        return self._table

    def add_bet(self, bet: Bet) -> None:
        existing_bets: list[Bet] = bet.already_placed_bets(self)
        new_bet = sum(existing_bets + [bet])
        amount_available_to_bet = self.bankroll + sum(x.amount for x in existing_bets)

        if new_bet.allowed(self) and new_bet.amount <= amount_available_to_bet:
            for bet in existing_bets:
                self.bets.remove(bet)
            self.bankroll -= bet.amount
            self.bets.append(new_bet)

    def get_bets_by_type(self, bet_type: typing.Type[Bet] | tuple[typing.Type[Bet], ...]):
        return [x for x in self.bets if isinstance(x, bet_type)]

    def remove_bet(self, bet: Bet) -> None:
        if bet in self.bets and bet.is_removable(self):
            self.bankroll += bet.amount
            self.bets.remove(bet)

    def add_strategy_bets(self) -> None:
        """ Implement the given betting strategy

        """
        if self.strategy is not None:
            self.strategy.update_bets(self)

    def update_bet(self, verbose: bool = False) -> None:
        for bet in self.bets[:]:
            result = bet.get_result(self.table)
            self.bankroll += result.bankroll_change

            if verbose:
                self.print_bet_update(bet, result)

            if result.remove:
                self.bets.remove(bet)

    def print_bet_update(self, bet: Bet, result: BetResult) -> None:
        if result.won:
            print(f"{self.name} won ${result.amount - bet.amount} on {bet}!")
        elif result.lost:
            print(f"{self.name} lost ${bet.amount} on {bet}.")

    def __repr__(self) -> str:
        return f'{self.name} - ${self.bankroll}'
