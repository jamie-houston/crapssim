import crapssim
from crapssim import Table
from crapssim.statistics.statistics import SimulatorStatistics
from crapssim.strategy.examples import *

if __name__ == '__main__':

    verbose = False
    # change_defaults = input("Change defaults? (default no) ").lower()[:1] == 'y'
    change_defaults = False
    def query(question, default):
        try:
            if change_defaults:
                return int(input(f"{question} (default {default}? ") or default)
        except Exception:
            pass
        return default

    max_shooters = query("Max Shooters", 10)
    n_sim = query("Number of simulations", 10)
    bankroll = query("Bankroll", 1000)
    base_unit = query("Base Unit", 25)

    all_strategies = {
        # BetPlace,
        # FieldWinProgression,
        BetDontPass,
        BetPassLine,
        DiceDoctor,
        HammerLock,
        IronCross,
        Knockout,
        Pass2Come,
        PassLinePlace68,
        PassLinePlace68Move59,
        # Place682Come,
        Place68CPR,
        Place68DontCome2Odds,
        Place68Move59,
        PlaceInside,
        Risk12,
        TwoCome,
                      }
    strategies = {strat.__name__: strat(base_unit) for strat in all_strategies}

    simulator = SimulatorStatistics(strategies, bankroll, total_simulations=n_sim)

    for i in range(n_sim):
        table = Table()
        for strategy in strategies:
            table.add_player(bankroll=bankroll, strategy=strategies[strategy], name=strategy)

        table.run(max_rolls=float("inf"), max_shooter=max_shooters, verbose=verbose,
                  update_after_roll=simulator.update_after_roll)
        for p in table.players:
            simulator.update_after_all_rolls(p)
    print(f"\n{n_sim} runs.  {max_shooters} max shooters")

    result_table = simulator.generate_table()
    print(result_table)
